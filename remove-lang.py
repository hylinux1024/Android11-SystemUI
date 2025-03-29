from lxml import etree
import os

def list_values_folders(root_dir="res-product"):
    """
    列出 root_dir 目录下所有以 "values" 开头的文件夹
    """
    values_folders = []

    if not os.path.exists(root_dir):
        print(f"目录不存在: {root_dir}")
        return values_folders

    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path) and entry.startswith("values"):
            values_folders.append(entry)

    return sorted(values_folders)

def remove_product_strings(xml_path):
    # 创建解析器（保留空白字符以维持格式）
    parser = etree.XMLParser(remove_blank_text=False, strip_cdata=False)

    # 解析 XML 并保留注释
    tree = etree.parse(xml_path, parser)
    root = tree.getroot()

    # 需要删除的 product 属性值
    target_products = {"tv", "tablet", "device"}

    # 定位所有需要删除的 string 标签
    for string_elem in root.xpath("//string[@product]"):
        if string_elem.get("product") in target_products:
            parent = string_elem.getparent()
            parent.remove(string_elem)

    # 序列化参数（保持原始格式）
    xml_str = etree.tostring(
        tree,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True,
        doctype="",
        with_comments=True  # 保留注释
    )

    # 手动修正缩进以匹配原始格式（四空格缩进）
    xml_str = xml_str.replace(b"  ", b"    ")  # 将双空格替换为四空格

    # 写回文件
    with open(xml_path, "wb") as f:
        f.write(xml_str)

# 删除 SystemUI/res-product 目录相同的 key
langs = list_values_folders()
for value_lang in langs:
    remove_product_strings(f"res-product/{value_lang}/strings.xml")
