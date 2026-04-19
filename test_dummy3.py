import sys

filepath = "python/packages/autogen-ext/src/autogen_ext/models/llama_cpp/_llama_cpp_completion_client.py"

with open(filepath, "r") as f:
    content = f.read()

import_block = """from llama_cpp import (
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
)"""

replacement_block = """import typing
from typing import Any, Callable, TypeVar, cast
try:
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
except ImportError:
    ChatCompletionFunctionParameters = Any  # type: ignore
    ChatCompletionRequestAssistantMessage = Any  # type: ignore
    ChatCompletionRequestFunctionMessage = Any  # type: ignore
    ChatCompletionRequestSystemMessage = Any  # type: ignore
    ChatCompletionRequestToolMessage = Any  # type: ignore
    ChatCompletionRequestUserMessage = Any  # type: ignore
    ChatCompletionTool = Any  # type: ignore
    ChatCompletionToolFunction = Any  # type: ignore
    Llama = Any  # type: ignore
    llama_chat_format = Any  # type: ignore"""

content = content.replace(import_block, replacement_block)

with open(filepath, "w") as f:
    f.write(content)
