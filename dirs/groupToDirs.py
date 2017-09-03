import argparse
import os


def f(path_dir):
    i = 0
    while True:
        files = os.listdir(path)
        while i < len(files):
            name = files[i].split(sep=" (")
            name.sort(reverse=True)
            if len(name) > 1:
                name = name[0]
                os.mkdir(name)
                os.system('move "*' + name + '*" "' + name + '"')
                break
            i += 1
        if i == len(files):
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str, help="input path dir")
    args = parser.parse_args()
    path = args.path
    os.system('cd /d  path')
    os.chdir(path)
    f(path)
