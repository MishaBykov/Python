import argparse
import re
import os
from collections.abc import Callable

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
TITLE = EMFictionBook.title
TRANSLATOR = EMFictionBook.translator
NICKNAME = EMFictionBook.nickname
SEQUENCE = EMFictionBook.sequence
TR = EMFictionBook.tr
TD = EMFictionBook.td

namespace_xlink: str = "http://www.w3.org/1999/xlink"
namespace_fiction_book: str = "http://www.gribuser.ru/xml/fictionbook/2.0"

new_genres = ['network_literature', 'sf_action', 'sf_heroic']
new_author = {
    'first-name': 'Nam',
    'last-name': 'Heesung'
}
translator_nickname = 'Captain'
new_annotation = 'Книга о виртуальной реальности. Главный герой Хэн стремится всеми силами выплыть из бедности ' \
                 'благодаря компьютерной игре. Бестселлер. '
sequence_name = 'Легендарный Лунный Скульптор'


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


def extract_sequence_value(title_info: etree.ElementBase) -> int | None:
    book_title_path = './{*}book-title'
    book_title: etree.ElementBase = title_info.find(book_title_path)
    if book_title is None:
        print(tag_not_found_message.format(book_title_path))
        return None
    return int(book_title.text.split()[-1])


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

    title_info.append(
        TRANSLATOR(
            NICKNAME(translator_nickname)
        )
    )
    title_info.append(
        SEQUENCE(name=sequence_name, number=str(extract_sequence_value(title_info)))
    )


def fix_document_info(document_info: etree.ElementBase):
    author_tag: etree.ElementBase = document_info.find('./{*}author')
    author_tag.insert(0, LAST_NAME())
    author_tag.insert(0, FIRST_NAME())


def fix_coverpage(root_element: etree.ElementBase):
    coverpage_image_abs_path = '/{*}description/{*}title-info/{*}coverpage/{*}image'
    image_tag: etree.ElementBase = root_element.getroottree().find(coverpage_image_abs_path)
    if image_tag is None:
        print(tag_not_found_message.format(coverpage_image_abs_path))
        return
    attrib_name = etree.QName(namespace_xlink, 'href')
    image_name = image_tag.attrib[attrib_name.text].lstrip('#')

    binary_tag: etree.ElementBase = root_element.getroottree().find('/{*}binary/[@id="' + image_name + '"]')

    new_id = 'cover'
    binary_tag.attrib['id'] = new_id
    image_tag.attrib[attrib_name.text] = '#' + new_id


def fix_section_title(body_tag: etree.ElementBase):
    titles = body_tag.xpath("//*[re:match(text(), 'Глава [0-9][0-9]?\\..*')]",
                            namespaces={"re": "http://exslt.org/regular-expressions"})

    for element in titles:
        title_text = element.text
        find_tag = ''.join(['{', namespace_fiction_book, '}', 'section'])
        while element.getparent().tag != find_tag:
            element = element.getparent()

        section: etree.ElementBase = element.getparent()
        section.remove(element)
        section.insert(0, TITLE(P(title_text)))


def fix_body(body_tag: etree.ElementBase):
    for p in body_tag.iter("{*}p"):
        p: etree.ElementBase
        if p.text.isspace() and len(p) == 0:
            p.getparent().remove(p)

    fix_section_title(body_tag)

    tables = body_tag.findall('./{*}section/{*}table')

    for table in tables:
        table: etree.ElementBase
        if len(table) != 1:
            print("skip table: " + table.tag)
            continue
        tr = table.getchildren()[0]
        if len(tr) != 1:
            print("skip table: " + table.tag)
            continue
        td: etree.ElementBase = tr.getchildren()[0]
        td_text = td.text
        table.clear()
        for line in td_text.split('\n'):
            if line.isspace():
                continue
            table.append(TR(TD(line)))


def fix_tag(parent_element: etree.ElementBase, find_path: str, fix_method: Callable[[etree.ElementBase], None]):
    title_info: etree.ElementBase = parent_element.find(find_path)
    if title_info is None:
        print(tag_not_found_message.format(find_path))
    else:
        fix_method(title_info)


def add_section(xml: str) -> str:
    result = xml
    titles = re.findall('(Глава [0-9][0-9]?\\..*?)<', xml)
    for i in range(1, len(titles)):
        ind_title = result.find(titles[i])
        ind_p_before = result.rfind('<p>', 0, ind_title)
        result = ''.join([result[:ind_p_before], '</section><section>', result[ind_p_before:]])
    return result


def fix_xml(xml: str) -> bytes:
    result = xml.replace('﻿', '').replace(' ', '')
    result = fix_syntax_xml_table(result)
    result = add_section(result)

    root_tree: etree.ElementBase = etree.fromstring(result.encode(encoding='utf-8'))

    print("root tag = " + root_tree.tag)

    stylesheet: etree.ElementBase = root_tree.find("{*}stylesheet")
    if stylesheet is not None:
        print('remove: ' + stylesheet.tag)
        stylesheet.getparent().remove(stylesheet)

    fix_tag(root_tree, './{*}description/{*}title-info', fix_title_info)

    fix_coverpage(root_tree)

    fix_tag(root_tree, './{*}description/{*}document-info', fix_document_info)

    fix_tag(root_tree, './{*}body', fix_body)

    return etree.tostring(root_tree, encoding="utf-8", xml_declaration=True)


def fix_fb2(path_book: str, path_result: str):
    print('path_book: ' + path_book)

    text_file: str
    with open(path_book, "r", encoding="utf-8") as file:
        text_file = file.read()

    fixed_xml = fix_xml(text_file)

    with open(path_result, "wb") as file:
        file.write(fixed_xml)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_books', type=str)
    args = parser.parse_args()

    path_books = args.path_books

    files = os.listdir(path_books)

    for file_name in files:
        full_path = os.path.join(path_books, file_name)
        if os.path.isdir(full_path):
            continue
        if os.path.splitext(file_name)[1] != ".fb2":
            continue
        fix_fb2(full_path, full_path)
