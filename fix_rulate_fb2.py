from dataclasses import dataclass

from lxml.builder import ElementMaker
from lxml import etree

tag_not_found_message = "tag with path ({}) not found"

EMFictionBook = ElementMaker(namespace="http://www.gribuser.ru/xml/fictionbook/2.0",
                             nsmap={'l': "http://www.w3.org/1999/xlink"})
GENRE = EMFictionBook.genre
AUTHOR = EMFictionBook.author
FIRST_NAME = getattr(EMFictionBook, 'first-name')
LAST_NAME = getattr(EMFictionBook, 'last-name')
ANNOTATION = EMFictionBook.annotation
P = EMFictionBook.p
SECTION = EMFictionBook.section


@dataclass(frozen=True)
class Namespaces:
    fictionBook: str = "http://www.gribuser.ru/xml/fictionbook/2.0"
    xlink: str = "http://www.w3.org/1999/xlink"


path_book = r'D:\repos\lms\Легендарный_Лунный_Скульптор_Том_01.fb2'
path_result = r"D:\repos\lms\output.fb2"
new_genres = ['network_literature', 'sf_action', 'sf_heroic']
new_author = {
    'first-name': 'Nam',
    'last-name': 'Heesung'
}
new_annotation = 'Книга о виртуальной реальности. Главный герой Хэн стремится всеми силами выплыть из бедности ' \
                 'благодаря компьютерной игре. Бестселлер. '
new_sequence_name = 'Легендарный Лунный Скульптор'


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


def fix_genre(title_info: etree.ElementBase):
    genres = title_info.findall('{*}genre')

    for genre in genres:
        print("remove: " + genre.tag)
        genre.getparent().remove(genre)

    for new_genre in reversed(new_genres):
        title_info.insert(0, GENRE(new_genre))


def create_element_author() -> etree.ElementBase:
    return AUTHOR(
        FIRST_NAME(new_author['first-name']),
        LAST_NAME(new_author['last-name'])
    )


def create_element_annotation() -> etree.ElementBase:
    return ANNOTATION(
        P(
            new_annotation
        )
    )


def extract_sequence_value():
    pass


def fix_title_info(title_info: etree.ElementBase):
    fix_genre(title_info)

    author_tag = title_info.find('{*}author')
    title_info.replace(author_tag, create_element_author())

    book_title_path = '{*}book-title'
    book_title: etree.ElementBase = title_info.find(book_title_path)
    if book_title is None:
        print(tag_not_found_message.format(book_title_path))
    else:
        book_title.addnext(create_element_annotation())





def fix_document_info():
    pass


def fix_xml(xml: str) -> bytes:
    result = xml.replace('﻿', '').replace('  ', '')
    result = fix_syntax_xml_table(result)
    root_tree: etree.ElementBase = etree.fromstring(result.encode(encoding='utf-8'))

    print("root tag = " + root_tree.tag)

    stylesheet: etree.ElementBase = root_tree.find("{*}stylesheet")
    if stylesheet is not None:
        print('remove: ' + stylesheet.tag)
        stylesheet.getparent().remove(stylesheet)

    title_info_path = './{*}description/{*}title-info'
    title_info: etree.ElementBase = root_tree.find(title_info_path)
    if title_info is None:
        print(tag_not_found_message.format(title_info_path))
    else:
        fix_title_info(title_info)

    # fix_coverpage(root_tree)

    return etree.tostring(root_tree, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    text_file: str
    with open(path_book, "r", encoding="utf-8") as file:
        text_file = file.read()

    fixed_xml = fix_xml(text_file)

    with open(path_result, "wb") as file:
        file.write(fixed_xml)
