import argparse
import os
import shutil as sh

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str, help="input path dir")
    args = parser.parse_args()
    path = args.path
    os.chdir(path)
    files = os.listdir(path)
    files.sort(reverse=True)
    for file in files:
        if '(' not in file:
            continue
        name_file = str(file)
        name_dir = str(file.split(sep="(")[0].strip())
        if len(name_dir) > 0:
            if not os.path.exists(name_dir):
                os.mkdir(name_dir)
            sh.move(name_file, str(name_dir))
