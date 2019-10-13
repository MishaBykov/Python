import argparse
import os
import shutil as sh


def f(path_dir):
    files = os.listdir(path)
    files.sort(reverse=True)
    for file in files:
        name_file = str(file)
        name_dir = str(file.split(sep="(")[0].strip())
        if len(name_dir) > 1:
            try:
                os.mkdir(name_dir)
            except FileExistsError:
                pass
            sh.move(name_file, str(name_dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str, help="input path dir")
    args = parser.parse_args()
    path = args.path
    os.system('cd /d "' + path + '"')
    os.chdir(path)
    f(path)
