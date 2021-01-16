import argparse
from rename.Renamer import Renamer
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Files to dirs (ext)')
    parser.add_argument("path", type=str,
                        help="input path dir")
    args = parser.parse_args()
    path = args.path

    os.chdir(path)
    renamer = Renamer(path)
    entry: os.DirEntry
    for entry in sorted(filter(lambda x: '.' in x.name, os.scandir(path)),
                        key=lambda x: x.name.rsplit('.', maxsplit=1)[1]):
        if not entry.is_file():
            continue
        dir_name = os.path.splitext(entry.name)[1].replace('.', '')
        if dir_name.replace('.', '') == "":
            continue

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        renamer.destination_path = os.path.join(path, dir_name)
        renamer.rename(entry.name)
