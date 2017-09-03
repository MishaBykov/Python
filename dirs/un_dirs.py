import argparse
import os


def new_name(old_name, ins):
    ins = '(' + str(ins) + ')'
    old_name = old_name.rsplit('.', 1)
    old_name[0] = old_name[0] + ' ' + ins
    return str.join('.', old_name)


def move(src, dst, a=0):
    name = src.rsplit('\\', 1)[-1]
    while True:
        try:
            os.rename(src, os.path.join(dst, (name if a == 0 else (new_name(name, a)))))
            break
        except FileExistsError:
            a += 1
    if a == 0:
        return None
    else:
        return name


def main():
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str,
                        help="input path dir")
    args = parser.parse_args()
    path = args.path

    zeros = set()
    for file in os.scandir(path):
        if file.is_dir():
            for f in os.scandir(file.path):
                zeros.add(move(f.path, path))
            os.rmdir(file.path)
    if None in zeros:
        zeros.remove(None)
    for zero in zeros:
        try:
            os.rename(os.path.join(path, zero), os.path.join(path, new_name(zero, 0)))
        except FileExistsError:
            move(os.path.join(path, zero), path, a=1)


if __name__ == '__main__':
    main()
