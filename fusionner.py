import re
from bs4 import BeautifulSoup
from pathlib import Path

def extract_content(file_paths):
    style_dict = {}
    body_dict = {}

    for file_path in file_paths:
        path = Path(file_path)
        filename = path.stem

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'lxml')
        
        style_content = '\n'.join(tag.string for tag in soup.find_all('style') if tag.string)
        body_content = soup.body.decode_contents() if soup.body else ''

        style_dict[filename] = style_content
        body_dict[filename] = body_content

    return style_dict, body_dict

def chk_cls(style_dict, input_files):
    tgt_cls = {'.A', '.batch', '.REPLACED', '.CHANGED'}

    def extract_cls(style_content):
        extracted_classes = {f'.{name}' for name in re.findall(r'\.([A-Za-z0-9_-]+)', style_content)}
        filtered_classes = {cls for cls in extracted_classes if any(cls.startswith(prefix) for prefix in tgt_cls)}
        return filtered_classes

    cls_sets = [extract_cls(style) for style in style_dict.values()]

    for i in range(len(cls_sets)):
        for j in range(i + 1, len(cls_sets)):
            if cls_sets[i] & cls_sets[j]:
                return i, j 
    return None

def rename_batch_classes_in_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        html = file.read()
    
    pattern = r'(?<=class=["\'])([^"\']+)(?=["\'])'
    def replace_classes(match):
        classes = match.group().split()
        replaced = [cls.replace('batch', 'REPLACED', 1) if cls.startswith('batch') else cls for cls in classes]
        return ' '.join(replaced)
    
    updated_html = re.sub(pattern, replace_classes, html)
    
    pattern = r'(?<=\.)(batch\w*)'
    updated_html = re.sub(pattern, lambda m: m.group().replace('batch', 'REPLACED', 1), updated_html)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(updated_html)

def rename_a_classes_in_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        html = file.read()
    
    pattern = r'(?<=class=["\'])([^"\']+)(?=["\'])'
    def replace_classes(match):
        classes = match.group().split()
        replaced = [cls.replace('A', 'CHANGED', 1) if cls.startswith('A') else cls for cls in classes]
        return ' '.join(replaced)
    
    updated_html = re.sub(pattern, replace_classes, html)
    
    pattern = r'(?<=\.)(A\w*)'
    updated_html = re.sub(pattern, lambda m: m.group().replace('A', 'CHANGED', 1), updated_html)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(updated_html)

#for three files we need this combine function 

def combine_files(file_one, file_two, file_three):
    input_files = [file_one, file_two, file_three]
    style_dict, body_dict = extract_content(input_files)

    result = chk_cls(style_dict, input_files)

    if result is not None:
        i, j = result  
        rename_batch_classes_in_file(input_files[i], f"modified_batch_{i}.html")
        rename_a_classes_in_file(input_files[i], f"modified_A_{i}.html")
        
        updated_file = f"modified_batch_{i}.html"  
        input_files[i] = updated_file
        style_dict, body_dict = extract_content(input_files)  

    styles = '\n'.join([style_dict[Path(path).stem] for path in input_files])
    body_content = ''.join([body_dict[Path(path).stem] for path in input_files])

    path_two = Path(file_two)
    with open(path_two, 'r', encoding='utf-8') as f:
        content_two = f.read()

    soup_two = BeautifulSoup(content_two, 'lxml')

    if soup_two.head:
        style_tag = soup_two.head.find('style')
        if style_tag:
            style_tag.string = styles
        else:
            new_style_tag = soup_two.new_tag('style')
            new_style_tag.string = styles
            soup_two.head.append(new_style_tag)
    
    if soup_two.body:
        soup_two.body.clear()
        soup_two.body.append(BeautifulSoup(body_content, 'lxml'))

    output_file = path_two.parent / "merged_output.xhtml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup_two))

#for two files this is what we need 
def combine_filestwo(file_one, file_two):
    input_files = [file_one, file_two]  # Adjusting for two files
    style_dict, body_dict = extract_content(input_files)

    result = chk_cls(style_dict, input_files)

    if result is not None:
        i, j = result
        rename_batch_classes_in_file(input_files[i], f"modified_batch_{i}.html")
        rename_a_classes_in_file(input_files[i], f"modified_A_{i}.html")
        
        updated_file = f"modified_batch_{i}.html"
        input_files[i] = updated_file
        style_dict, body_dict = extract_content(input_files)

    styles = '\n'.join([style_dict[Path(path).stem] for path in input_files])
    body_content = ''.join([body_dict[Path(path).stem] for path in input_files])

    path_two = Path(file_two)
    with open(path_two, 'r', encoding='utf-8') as f:
        content_two = f.read()

    soup_two = BeautifulSoup(content_two, 'lxml')

    if soup_two.head:
        style_tag = soup_two.head.find('style')
        if style_tag:
            style_tag.string = styles
        else:
            new_style_tag = soup_two.new_tag('style')
            new_style_tag.string = styles
            soup_two.head.append(new_style_tag)
    
    if soup_two.body:
        soup_two.body.clear()
        soup_two.body.append(BeautifulSoup(body_content, 'lxml'))

    output_file = path_two.parent / "merged_output.xhtml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup_two))

file_one = r"C:\Users\norel_2b285at\Downloads\IDI 5 AVRIL 2025 A FUSIONNER\IDI 5 AVRIL 2025 A FUSIONNER\PARTIE 1.xhtml"
file_two = r"C:\Users\norel_2b285at\Downloads\IDI 5 AVRIL 2025 A FUSIONNER\IDI 5 AVRIL 2025 A FUSIONNER\87_114.xhtml"
#combine_filestwo(file_one, file_two)

file_one = r"C:\Users\norel_2b285at\Downloads\IDI 5 AVRIL 2025 A FUSIONNER\IDI 5 AVRIL 2025 A FUSIONNER\PARTIE 1.xhtml"
file_two = r"C:\Users\norel_2b285at\Downloads\IDI 5 AVRIL 2025 A FUSIONNER\IDI 5 AVRIL 2025 A FUSIONNER\87_114.xhtml"
file_three = r"C:\Users\norel_2b285at\Downloads\IDI 5 AVRIL 2025 A FUSIONNER\IDI 5 AVRIL 2025 A FUSIONNER\PARTIE 3.xhtml"
combine_files(file_one, file_two, file_three)
