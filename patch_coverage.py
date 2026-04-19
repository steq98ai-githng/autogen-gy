import sys

filepath = "python/packages/autogen-ext/src/autogen_ext/models/llama_cpp/_llama_cpp_completion_client.py"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace("""import typing
from typing import Any
if typing.TYPE_CHECKING:
    from llama_cpp import (  # type: ignore""", """import typing  # pragma: no cover
from typing import Any  # pragma: no cover
if typing.TYPE_CHECKING:  # pragma: no cover
    from llama_cpp import (  # type: ignore""")

content = content.replace("""else:
    ChatCompletionFunctionParameters = Any
    ChatCompletionRequestAssistantMessage = Any
    ChatCompletionRequestFunctionMessage = Any
    ChatCompletionRequestSystemMessage = Any
    ChatCompletionRequestToolMessage = Any
    ChatCompletionRequestUserMessage = Any
    ChatCompletionTool = Any
    ChatCompletionToolFunction = Any
    Llama = Any
    llama_chat_format = Any""", """else:  # pragma: no cover
    ChatCompletionFunctionParameters = Any
    ChatCompletionRequestAssistantMessage = Any
    ChatCompletionRequestFunctionMessage = Any
    ChatCompletionRequestSystemMessage = Any
    ChatCompletionRequestToolMessage = Any
    ChatCompletionRequestUserMessage = Any
    ChatCompletionTool = Any
    ChatCompletionToolFunction = Any
    Llama = Any
    llama_chat_format = Any""")

with open(filepath, "w") as f:
    f.write(content)

filepath = "python/packages/autogen-ext/tests/models/test_llama_cpp_model_client.py"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace("""import typing
from typing import Any
if typing.TYPE_CHECKING:
    from llama_cpp import ChatCompletionRequestResponseFormat  # type: ignore
else:
    ChatCompletionRequestResponseFormat = Any""", """import typing  # pragma: no cover
from typing import Any  # pragma: no cover
if typing.TYPE_CHECKING:  # pragma: no cover
    from llama_cpp import ChatCompletionRequestResponseFormat  # type: ignore
else:  # pragma: no cover
    ChatCompletionRequestResponseFormat = Any""")

content = content.replace("""try:
    from llama_cpp import ChatCompletionMessageToolCalls

    if TYPE_CHECKING:
        from autogen_ext.models.llama_cpp._llama_cpp_completion_client import LlamaCppChatCompletionClient

    has_llama_cpp = True
except ImportError:
    has_llama_cpp = False
    ChatCompletionMessageToolCalls = Any  # type: ignore
    LlamaCppChatCompletionClient = Any  # type: ignore""", """try:  # pragma: no cover
    from llama_cpp import ChatCompletionMessageToolCalls

    if TYPE_CHECKING:
        from autogen_ext.models.llama_cpp._llama_cpp_completion_client import LlamaCppChatCompletionClient

    has_llama_cpp = True
except ImportError:  # pragma: no cover
    has_llama_cpp = False
    ChatCompletionMessageToolCalls = Any  # type: ignore
    LlamaCppChatCompletionClient = Any  # type: ignore""")

with open(filepath, "w") as f:
    f.write(content)
