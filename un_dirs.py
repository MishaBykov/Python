import argparse
from Renamer import Renamer
import os


def move_all_from_dir(src, dst):
    renamer = Renamer(src, new_path=dst)
    for file in os.listdir(src):
        renamer.rename(file)
    del renamer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str, help="input path dir")
    args = parser.parse_args()
    for file in os.scandir(args.path):
        if file.is_dir():
            move_all_from_dir(file.path, args.path)
            os.rmdir(file.path)
