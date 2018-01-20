import argparse
import shutil as sh
import rename as r
import os


def move_all_from_dir(src, dst):
    for file in os.listdir(src):
        try:
            sh.move(os.path.join(src, file), dst)
        except sh.Error:
            r.rename(src, file, new_path=dst)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str, help="input path dir")
    args = parser.parse_args()
    for file in os.scandir(args.path):
        if file.is_dir():
            move_all_from_dir(file.path, args.path)
            os.rmdir(file.path)
