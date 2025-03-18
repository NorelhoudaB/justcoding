file_path = r"C:\Users\norel_2b285at\Downloads\WEN_URD_2024_FR_XHTML_25-03-17.html"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

# Replace &#xa0; with a normal space
content = content.replace("&#xa0;", " ")

with open(file_path, "w", encoding="utf-8") as file:
    file.write(content)

print("Replacement done successfully!")
