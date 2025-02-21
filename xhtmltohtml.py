from lxml import etree

def xhtml_to_html(xhtml_file, html_file):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(xhtml_file, parser)
    
    for elem in tree.xpath('//@*'):  
        if elem is None:
            elem.getparent().remove(elem)
    
    html_content = etree.tostring(tree, method="html", encoding="unicode")
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)


xhtml_to_html(r"C:\Users\norel_2b285at\Downloads\xhtml\JC_DECAUX_DEU_2024_CH5_FR_2_États financiers consolidés.xhtml", "output.html")
