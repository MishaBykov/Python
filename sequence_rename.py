# -*- coding: utf-8 -*-
import argparse
import os
import xml.etree.ElementTree as ET

from rename.Renamer import Renamer


def find_sequence(xml_file: str):
    xpath = ".//{*}description/{*}title-info/{*}sequence"
    try:
        root = ET.parse(xml_file).getroot()
    except ET.ParseError as e:
        print('[ParseError\n' + str(e.msg) + "\n" + xml_file + ']')
        return None
    sequence = root.find(xpath)
    return sequence.attrib if sequence is not None else {'name': 'not sequence'}


def dir_root_books(dir_path: str):
    entry: os.DirEntry
    entries = list(os.scandir(dir_path))
    sequence_files_fb2 = {}
    for entry in entries:
        if entry.is_dir():
            dir_root_books(entry.path)
        else:
            ext = os.path.splitext(entry.name)[-1]
            if ext == '.fb2':
                sequence = find_sequence(entry.path)
                if sequence is None:
                    continue
                if sequence["name"] in sequence_files_fb2:
                    sequence_files_fb2[sequence["name"]].append((entry, sequence))
                else:
                    sequence_files_fb2[sequence["name"]] = [(entry, sequence)]

    r = Renamer(dir_path)
    for key in sequence_files_fb2:
        for entry, sequence in sequence_files_fb2[key]:
            number = (" " + sequence["number"]) if "number" in sequence else ""
            r.rename(entry.name, sequence["name"] + number + ".fb2")
    if len(sequence_files_fb2) == 1:
        sequence_name = list(sequence_files_fb2.keys())[0]
        if os.path.basename(dir_path) != sequence_name:
            r = Renamer(os.path.dirname(dir_path))
            r.rename(os.path.basename(dir_path), sequence_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Name part replacement')
    parser.add_argument("-drp", "--dit_root_path", type=str, help="input path")
    args = parser.parse_args()

    dir_root_books(args.dit_root_path)
