import chardet

with open(r"", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    print(result["encoding"])

with open(r"", "r", encoding="utf-8-sig") as f:
    content = f.read()

with open(r"C:\Users", "w", encoding="utf-8") as f:
    f.write(content)
