import re

def rename_classes_in_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        html = file.read()
    
    pattern = r'(?<=class=")[^"]+|(?<=class=\')[^\']+'
    def replace_classes(match):
        classes = match.group().split()
        return ' '.join(cls.replace('A', 'ALPHA', 1) if cls.startswith('A') else cls for cls in classes)
    
    updated_html = re.sub(pattern, replace_classes, html)
    
    pattern = r'(?<=\.)(A\w*)'
    updated_html = re.sub(pattern, lambda m: m.group().replace('A', 'ALPHA', 1), updated_html)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(updated_html)

input_html_file = r"C:\Users\norel_2b285at\Downloads\New folder\partie1e.html"
output_html_file = "output.html"
rename_classes_in_file(input_html_file, output_html_file)
