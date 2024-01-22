import lxml.etree as ET

ET.register_namespace = {"http://www.w3.org/1999/xlink": "",
                         "http://www.gribuser.ru/xml/fictionbook/2.0": ""}

path_book = r'D:\repos\lms\Легендарный_Лунный_Скульптор_Том_01.fb2'
path_result = r"D:\repos\lms\output.fb2"


def fix_syntax_xml_table(xml: str) -> str:
    result = xml
    begin_i = 0
    while True:
        tag_open_table_i = result.find("<table>", begin_i)
        tag_close_table_i = result.find("</table>", tag_open_table_i)
        if tag_open_table_i == -1 or tag_close_table_i == -1:
            break
        table = result[tag_open_table_i: tag_close_table_i].replace("<p>", "").replace("</p>", "")
        result = result[:tag_open_table_i] + table + result[tag_close_table_i:]
        begin_i = tag_open_table_i + len(table)

    return result


def fix_xml(xml: str) -> str:
    result = xml.replace('﻿', '')
    result = result.replace('  ', '')
    result = fix_syntax_xml_table(result)

    return result


if __name__ == '__main__':
    text_file: str
    with open(path_book, "r", encoding="utf-8") as file:
        text_file = file.read()

    fixed_xml = fix_xml(text_file)

    element_tree = ET.fromstring(fixed_xml.encode(encoding='utf-8'))

    with open(path_result, "wb") as file:
        file.write(ET.tostring(element_tree, encoding="utf-8", xml_declaration=True))
