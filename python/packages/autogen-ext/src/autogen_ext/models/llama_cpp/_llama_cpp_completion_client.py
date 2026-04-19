import asyncio
import logging
import re
import warnings
from typing import Any, AsyncGenerator, Dict, List, Literal, Mapping, Optional, Sequence, TypedDict, Union, cast, TYPE_CHECKING

from autogen_core import EVENT_LOGGER_NAME, CancellationToken, FunctionCall, MessageHandlerContext
from autogen_core.logging import LLMCallEvent
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    CreateResult,
    FinishReasons,
    FunctionExecutionResultMessage,
    LLMMessage,
    ModelFamily,
    ModelInfo,
    RequestUsage,
    SystemMessage,
    UserMessage,
    validate_model_info,
)
from autogen_core.tools import Tool, ToolSchema

if TYPE_CHECKING:
    from llama_cpp import (
        ChatCompletionFunctionParameters,
        ChatCompletionRequestAssistantMessage,
        ChatCompletionRequestFunctionMessage,
        ChatCompletionRequestSystemMessage,
        ChatCompletionRequestToolMessage,
        ChatCompletionRequestUserMessage,
        ChatCompletionTool,
        ChatCompletionToolFunction,
        Llama,
        llama_chat_format,
    )
from pydantic import BaseModel
from typing_extensions import Unpack

logger = logging.getLogger(EVENT_LOGGER_NAME)


class LlamaCppParams(TypedDict, total=False):
    # Extracted from `__init__` from https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.Llama.__init__
    repo_id: Optional[str]
    filename: Optional[str]
    additional_files: Optional[List[Any]]
    local_dir: Optional[str]
    local_dir_use_symlinks: Union[bool, Literal["auto"]]
    cache_dir: Optional[str]

    model_path: str
    n_gpu_layers: int
    split_mode: int
    main_gpu: int
    tensor_split: Optional[List[float]]
    rpc_servers: Optional[str]
    vocab_only: bool
    use_mmap: bool
    use_mlock: bool
    kv_overrides: Optional[Dict[str, Union[bool, int, float, str]]]
    seed: int
    n_ctx: int
    n_batch: int
    n_ubatch: int
    n_threads: Optional[int]
    n_threads_batch: Optional[int]
    rope_scaling_type: Optional[int]
    pooling_type: int
    rope_freq_base: float
    rope_freq_scale: float
    yarn_ext_factor: float
    yarn_attn_factor: float
    yarn_beta_fast: float
    yarn_beta_slow: float
    yarn_orig_ctx: int
    logits_all: bool
    embedding: bool
    offload_kqv: bool
    flash_attn: bool
    no_perf: bool
    last_n_tokens_size: int
    lora_base: Optional[str]
    lora_scale: float
    lora_path: Optional[str]
    numa: Union[bool, int]
    chat_format: Optional[str]
    chat_handler: Optional[Any]
    draft_model: Optional[Any]
    tokenizer: Optional[Any]
    type_k: Optional[int]
    type_v: Optional[int]
    spm_infill: bool
    verbose: bool


def convert_tools(tools: Sequence[Union[Tool, ToolSchema]]) -> Any:
    result: Any = []
    for tool in tools:
        if isinstance(tool, Tool):
            tool_schema = tool.schema
        else:
            tool_schema = tool

        tool_param: Dict[str, Any] = {
            "type": "function",
            "function": {
                "name": tool_schema["name"],
                "description": tool_schema["description"] if "description" in tool_schema else "",
                "parameters": tool_schema["parameters"] if "parameters" in tool_schema else {},
            },
        }

        result.append(cast(Any, tool_param))

    return result


def assert_valid_name(name: str) -> str:
    """
    Ensure that the name is valid. If not, replace invalid characters with underscores.
    """
    if not re.match(r"^[a-zA-Z0-9_-]{1,64}$", name):
        warnings.warn(
            f"Invalid name '{name}'. Replacing invalid characters with underscores.", UserWarning, stacklevel=2
        )
        return re.sub(r"[^a-zA-Z0-9_-]", "_", name)[:64]
    return name


class LlamaCppChatCompletionClient(ChatCompletionClient):
    """
    A ChatCompletionClient that uses `llama_cpp.Llama` to generate text.

    To use this client, you must install the `llama-cpp` extra:
        `pip install "autogen-ext[llama-cpp]"`

    Args:
        model (str): Name of the model. Used only for configuration but unused by the client.
        model_info (ModelInfo, optional): Information about the model.
        **kwargs: Additional parameters to pass to `llama_cpp.Llama`. See
            [LlamaCppParams](https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.Llama.__init__)
            for supported parameters.

    """

    def __init__(
        self,
        model: str = "llama-cpp-python-model",
        model_info: Optional[ModelInfo] = None,
        **kwargs: Unpack[LlamaCppParams],
    ):
        try:
            from llama_cpp import Llama
        except ImportError as e:
            raise ImportError(
                "Please install llama-cpp-python: "
                "pip install autogen-ext[llama-cpp]"
                "or "
                "pip install llama-cpp-python"
            ) from e

        self.model = model

        if model_info is None:
            self._model_info = ModelInfo(
                vision=False, function_calling=True, json_output=True, family=ModelFamily.UNKNOWN
            )
        else:
            self._model_info = model_info

        validate_model_info(self._model_info)

        # Check if chat handler is provided
        chat_handler = kwargs.pop("chat_handler", None)
        self.chat_handler: Any = chat_handler

        self.llm = Llama(**kwargs)

        self._actual_usage = 0

    async def create(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = [],
        json_output: Optional[bool] = None,
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: Optional[CancellationToken] = None,
    ) -> CreateResult:
        if "tool_choice" in extra_create_args:
            logger.warning("tool_choice parameter specified but may not be supported by llama-cpp-python")

        converted_messages: Any = []
        for message in messages:
            if isinstance(message, SystemMessage):
                converted_messages.append({"role": "system", "content": message.content})
            elif isinstance(message, UserMessage):
                if isinstance(message.content, str):
                    converted_messages.append({"role": "user", "content": message.content})
                else:
                    raise NotImplementedError("llama-cpp-python only supports string content")
            elif isinstance(message, AssistantMessage):
                msg: Dict[str, Any] = {
                    "role": "assistant",
                    "content": message.content if isinstance(message.content, str) else "",
                }
                if hasattr(message, "name") and message.name:
                    msg["name"] = assert_valid_name(message.name)
                converted_messages.append(msg)
            elif isinstance(message, FunctionExecutionResultMessage):
                for call in message.content:
                    converted_messages.append(
                        {
                            "role": "tool",
                            "name": assert_valid_name(call.call_id),
                            "content": call.content,
                            "tool_call_id": assert_valid_name(call.call_id),
                        }
                    )
            else:
                raise NotImplementedError(f"Unsupported message type: {type(message)}")

        create_args = dict(extra_create_args)

        if tools:
            create_args["tools"] = convert_tools(tools)

        if json_output:
            create_args["response_format"] = {"type": "json_object"}

        response_future: Any = asyncio.Future()

        def create_chat_completion() -> Any:
            try:
                result = self.llm.create_chat_completion(messages=converted_messages, stream=False, **create_args)
                response_future.set_result(result)
            except Exception as e:
                response_future.set_exception(e)

        loop = asyncio.get_running_loop()
        task = loop.run_in_executor(None, create_chat_completion)

        if cancellation_token is not None:
            cancellation_token.link_future(response_future)

        response: Any = await response_future

        if hasattr(MessageHandlerContext, "logger"):
            # Use the autogen_core.logging logger if available
            msg_logger = getattr(MessageHandlerContext, "logger")()
            if msg_logger is not None:
                msg_logger.log_structured(
                    LLMCallEvent(
                        prompt_tokens=response["usage"]["prompt_tokens"],
                        completion_tokens=response["usage"]["completion_tokens"],
                    )
                )

        response_tool_calls: Any = None
        if "tool_calls" in response["choices"][0]["message"] and response["choices"][0]["message"]["tool_calls"]:
            response_tool_calls = response["choices"][0]["message"]["tool_calls"]

        if response_tool_calls is not None and len(response_tool_calls) > 0:
            content: Union[str, List[FunctionCall]]
            response_text: Any = response["choices"][0]["message"].get("content", None)
            if response_text is not None and len(response_text) > 0:
                # We have both text and tool calls.
                raise ValueError("llama-cpp-python returned both text and tool calls. This is not supported.")
            else:
                content = []
                for tool_call in response_tool_calls:
                    if tool_call["type"] == "function":
                        name = tool_call["function"]["name"]
                        arguments = tool_call["function"]["arguments"]

                        content.append(
                            FunctionCall(
                                id=tool_call["id"],
                                arguments=arguments,
                                name=assert_valid_name(name),
                            )
                        )
                if len(content) == 0:
                    raise ValueError("llama-cpp-python returned no tool calls, but tool_calls is not None.")
        else:
            content = response["choices"][0]["message"]["content"]
            if content is None:
                content = ""

        # Finish reason
        finish_reason: FinishReasons = "stop"
        if response["choices"][0]["finish_reason"] == "tool_calls":
            finish_reason = "function_calls"
        elif response["choices"][0]["finish_reason"] == "length":
            finish_reason = "length"

        message_ret = AssistantMessage(
            content=content,
            source="assistant",
        )

        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]

        self._actual_usage += prompt_tokens + completion_tokens

        usage = RequestUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )

        return CreateResult(finish_reason=finish_reason, content=message_ret.content, usage=usage, cached=False)

    async def create_stream(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = [],
        json_output: Optional[bool] = None,
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: Optional[CancellationToken] = None,
    ) -> AsyncGenerator[Union[str, CreateResult], None]:
        raise NotImplementedError("llama-cpp-python does not support streaming with autogen yet")

    def actual_usage(self) -> Any:
        return {
            "prompt_tokens": 0,
            "completion_tokens": self._actual_usage,
        }

    def total_usage(self) -> RequestUsage:
        return RequestUsage(
            prompt_tokens=0,
            completion_tokens=self._actual_usage,
        )

    def count_tokens(self, messages: Sequence[LLMMessage], *, tools: Sequence[Tool | ToolSchema] = []) -> int:
        tokens: int = 0
        for message in messages:
            tokens += len(self.llm.tokenize(str(message.content).encode("utf-8")))

        if tools:
            for tool in tools:
                tokens += len(self.llm.tokenize(str(tool).encode("utf-8")))

        return tokens

    def remaining_tokens(self, messages: Sequence[LLMMessage], *, tools: Sequence[Tool | ToolSchema] = []) -> int:
        return max(0, self.llm.n_ctx() - self.count_tokens(messages, tools=tools))

    def capabilities(self) -> ModelInfo:
        return self._model_info

    @property
    def model_info(self) -> ModelInfo:
        return self._model_info

    def __getstate__(self) -> Dict[str, Any]:
        state = self.__dict__.copy()
        del state["llm"]
        return state

    def close(self) -> None:
        if self.llm is not None:
            self.llm.close()

