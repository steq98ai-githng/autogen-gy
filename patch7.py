with open("python/packages/autogen-ext/tests/code_executors/test_docker_jupyter_code_executor.py", "r") as f:
    content = f.read()

search = """    code_result = await _executor.execute_code_blocks(code_blocks, cancellation_token=CancellationToken())
    # Check if the file was created
    assert code_result.exit_code == 0"""

replace = """    code_result = await _executor.execute_code_blocks(code_blocks, cancellation_token=CancellationToken())
    # Check if the file was created
    assert code_result.exit_code == 0"""

if search in content:
    content = content.replace(search, replace)
    with open("python/packages/autogen-ext/tests/code_executors/test_docker_jupyter_code_executor.py", "w") as f:
        f.write(content)
    print("Patch successful")
else:
    print("Search string not found")
