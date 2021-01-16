import argparse
from rename.Renamer import Renamer
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str, help="input path dir")
    args = parser.parse_args()
    renamer = Renamer(destination_path=args.path)
    for i in os.scandir(args.path):
        if i.is_dir():
            renamer.source_path = i.path
            for j in os.listdir(i.path):
                renamer.rename(j)
            renamer.destination_delete_object(i.path)
    del renamer
