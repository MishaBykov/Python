# -*- coding: utf-8 -*-
import argparse
import os.path
import xml.etree.cElementTree as ET


def update_sequence_name_fb2(filename: str, new_sequence_name: str):
    ET.register_namespace('l', "http://www.w3.org/1999/xlink")
    ET.register_namespace('', "http://www.gribuser.ru/xml/fictionbook/2.0")
    xpath = ".//{*}description/{*}title-info/{*}sequence"

    tree = ET.ElementTree(file=filename)
    root = tree.getroot()
    sequence = root.find(xpath)
    if sequence is None:
        print(filename + " -> not found sequence")
        return
    sequence.attrib['name'] = new_sequence_name

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='UTF-8', xml_declaration=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     'in the folder with fb2 files update the name of the series as the folder name')
    parser.add_argument("-dp", "--dir_path", type=str, help="directory path")
    args = parser.parse_args()

    dir_path = args.dir_path
    dir_name = os.path.basename(dir_path)

    if not os.path.exists(dir_path):
        print("dir not exist")
        exit()
    for name in os.listdir(dir_path):
        if os.path.splitext(name)[1] != ".fb2":
            print(name + ': no .fb2')
            continue
        update_sequence_name_fb2(os.path.join(dir_path, name), dir_name)
