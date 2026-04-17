with open('python/samples/gitty/src/gitty/_db.py', 'r') as f:
    content = f.read()

content = content.replace("to_update = []", "to_update: list[tuple[str, str, str, int]] = []")
content = content.replace("to_insert = []", "to_insert: list[tuple[int, str, str, str]] = []")

with open('python/samples/gitty/src/gitty/_db.py', 'w') as f:
    f.write(content)
