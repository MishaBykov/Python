import argparse
from Rename import Rename
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str, help="input path dir")
    args = parser.parse_args()
    r = Rename(destination_path=args.path)
    for i in os.scandir(args.path):
        if i.is_dir():
            r.source_path = i.path
            for j in os.listdir(i.path):
                r.run(j)
            r.destination_delete_object(i.path)
    del r
