import sys

filepath = "python/packages/autogen-ext/src/autogen_ext/models/llama_cpp/_llama_cpp_completion_client.py"

with open(filepath, "r") as f:
    content = f.read()

import_block = """import typing
from typing import Any
if typing.TYPE_CHECKING:
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
    )"""

replacement_block = """import typing
from typing import Any
if typing.TYPE_CHECKING:
    from llama_cpp import (  # type: ignore
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

content = content.replace(import_block, replacement_block)

with open(filepath, "w") as f:
    f.write(content)


filepath = "python/packages/autogen-ext/tests/models/test_llama_cpp_model_client.py"

with open(filepath, "r") as f:
    content = f.read()

import_block2 = """if typing.TYPE_CHECKING:
    from llama_cpp import ChatCompletionRequestResponseFormat"""
replacement_block2 = """if typing.TYPE_CHECKING:
    from llama_cpp import ChatCompletionRequestResponseFormat  # type: ignore"""

content = content.replace(import_block2, replacement_block2)

with open(filepath, "w") as f:
    f.write(content)
