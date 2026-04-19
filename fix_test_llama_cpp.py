import re

file_path = 'python/packages/autogen-ext/tests/models/test_llama_cpp_model_client.py'
with open(file_path, 'r') as f:
    content = f.read()

# Move the top-level import to the try-except block so it doesn't fail right away.
content = content.replace('from llama_cpp import ChatCompletionRequestResponseFormat\n', '')
content = content.replace('from llama_cpp import ChatCompletionMessageToolCalls', 'from llama_cpp import ChatCompletionMessageToolCalls, ChatCompletionRequestResponseFormat')

with open(file_path, 'w') as f:
    f.write(content)
