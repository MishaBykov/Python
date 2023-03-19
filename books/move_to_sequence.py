# -*- coding: utf-8 -*-
import argparse
import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

from rename.Renamer import Renamer


def get_name_from_sequence(sequence: dict, ext: str) -> str | None:
    if sequence is None:
        return None
    if 'name' in sequence:
        name = sequence['name']
    else:
        return None
    if 'number' in sequence:
        number = sequence['number']
    else:
        number = ''
    return name + ' ' + number + ext


def get_name_ind(name: str, ins: int) -> str:
    ins = '({})'.format(ins)
    name, ext = os.path.splitext(name)
    if ' (' in name:
        name = name[:name.rfind(' (')]
    return name + ' ' + ins + ext


def find_sequence(xml_file: str):
    xpath = ".//{*}description/{*}title-info/{*}sequence"
    try:
        root = ET.parse(xml_file).getroot()
    except ET.ParseError as e:
        print('[ParseError\n' + e.msg + " " + xml_file + ']')
        return None
    sequence = root.find(xpath)
    return sequence.attrib if sequence is not None else None


def books_move_sequence(source_path: str, target_path: str):
    for root, dirs, files in os.walk(source_path):
        if len(files) == 0:
            continue
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext == '.fb2':
                source_file = os.path.join(root, file)
                sequence = find_sequence(source_file)
                if sequence is None:
                    if not zipfile.is_zipfile(source_file):
                        continue
                    with zipfile.ZipFile(source_file, 'r') as zip_ref:
                        zip_files = zip_ref.filelist
                        if len(zip_files) < 2:
                            zip_ref.extractall(root)
                            if len(zip_files) == 0:
                                continue
                        else:
                            print('many files in zip\n dir: ' + root + '\n' + 'zip: ' + file)
                            continue
                        source_file = os.path.join(root, zip_files.pop().filename)
                        sequence = find_sequence(source_file)
                    os.remove(os.path.join(root, file))

                if sequence is None or 'name' not in sequence:
                    sequence_path = os.path.join(target_path, 'not sequence')
                else:
                    sequence_path = os.path.join(target_path, sequence['name'])

                if not os.path.exists(sequence_path):
                    os.mkdir(sequence_path)
                destination_name = get_name_from_sequence(sequence, '.fb2')
                if os.path.exists(os.path.join(sequence_path, destination_name)):
                    i = 0
                    while os.path.exists(os.path.join(sequence_path, destination_name)):
                        i += 1
                        destination_name = get_name_ind(destination_name, i)
                shutil.move(source_file, os.path.join(sequence_path, destination_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='management books')
    parser.add_argument("-sp", "--source_path", type=str, help="source path")
    parser.add_argument("-tp", "--target_path", type=str, help="target path")
    args = parser.parse_args()

    books_move_sequence(args.source_path, args.target_path)
