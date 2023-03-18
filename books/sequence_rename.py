# -*- coding: utf-8 -*-
import argparse
import os
import xml.etree.cElementTree as ET
import time


def editXML(filename):
    """
    Редактируем XML файл.
    """
    ET.register_namespace('l', "http://www.w3.org/1999/xlink")
    ET.register_namespace('', "http://www.gribuser.ru/xml/fictionbook/2.0")
    xpath = ".//{*}description/{*}title-info/{*}sequence"

    tree = ET.ElementTree(file=filename)
    root = tree.getroot()

    sequence = root.find(xpath)

    sequence.attrib['name'] = 'Алхимик'

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='UTF-8', xml_declaration=True)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='management books')
    # parser.add_argument("-drp", "--dit_root_path", type=str, help="input path")
    # args = parser.parse_args()

    xml_file_path = '/home/misha/temp/Алхимик/Алхимик 1.fb2'

    editXML(xml_file_path)
