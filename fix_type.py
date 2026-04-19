import re

file_path = 'python/packages/autogen-ext/src/autogen_ext/models/llama_cpp/_llama_cpp_completion_client.py'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace('-> List["ChatCompletionTool"]:', '-> List[Any]:')
content = content.replace('result: List["ChatCompletionTool"] = []', 'result: List[Any] = []')
content = content.replace('cast("ChatCompletionFunctionParameters", tool_param)', 'cast(Any, tool_param)')
content = content.replace('self.chat_handler: Optional["llama_chat_format.LlamaChatCompletionHandler"] = chat_handler', 'self.chat_handler: Optional[Any] = chat_handler')
content = content.replace('        converted_messages: List[\n            Union[\n                "ChatCompletionRequestSystemMessage",\n                "ChatCompletionRequestUserMessage",\n                "ChatCompletionRequestAssistantMessage",\n                "ChatCompletionRequestToolMessage",\n                "ChatCompletionRequestFunctionMessage",\n            ]\n        ] = []', '        converted_messages: List[Any] = []')
content = content.replace('response_tool_calls: Optional[List["ChatCompletionMessageToolCalls"]] = None', 'response_tool_calls: Optional[List[Any]] = None')
content = content.replace('def actual_usage(self) -> int:', 'def actual_usage(self) -> Any:')

with open(file_path, 'w') as f:
    f.write(content)


file_path = 'python/packages/autogen-ext/tests/models/test_llama_cpp_model_client.py'
with open(file_path, 'r') as f:
    content = f.read()
content = content.replace('tools: Optional[List[ChatCompletionTool]] = None', 'tools: Optional[List[Any]] = None')
content = content.replace('response_format: Optional[ChatCompletionRequestResponseFormat] = None', 'response_format: Optional[Any] = None')
content = content.replace('ChatCompletionMessageToolCalls', 'Any')
content = content.replace('ChatCompletionRequestResponseFormat', 'Any')

with open(file_path, 'w') as f:
    f.write(content)
