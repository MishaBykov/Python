import os
import argparse
import re


def new_name(old_name, ins):
    ins = '(' + str(ins) + ')'
    old_name = old_name.rsplit('.', 1)
    old_name[0] = old_name[0] + ' ' + ins
    return str.join('.', old_name)


def rename(path, name, replace=None, regex=None, a=0):
    nn = ''
    if replace:
        nn = name.replace(replace[0], replace[1])
    elif regex:
        nn = re.sub(regex[0], regex[1], name)
    else:
        print("Ошибка\n", path, name, replace, regex)

    while True:
        try:
            os.rename(os.path.join(path, name), os.path.join(path, (new_name(nn, a))))
            break
        except FileExistsError:
            a += 1
        except OSError:
            break
    if a == 0:
        try:
            os.rename(os.path.join(path, (new_name(nn, a))), os.path.join(path, nn))
        except FileExistsError:
            os.rename(os.path.join(path, (new_name(nn, a))), os.path.join(path, (new_name(nn, a + 1))))
            os.rename(os.path.join(path, nn), os.path.join(path, (new_name(nn, a))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str, help="input path dir")
    parser.add_argument("-rp", "--replace", nargs=2,
                        help="input source")
    parser.add_argument("-rg", "--regex", nargs=2,
                        help="input replace")
    args = parser.parse_args()
    path_dir = args.path
    if args.regex is not None and args.replace is not None:
        n = int(input("Введите номер:\n1) replace\n2) regex\n"))
        if n == 1:
            args.regex = None
        elif n == 2:
            args.replace = None
        else:
            print("Exit\n")
            exit()
    if args.regex is None and args.replace is None:
        n = int(input("Введите номер:\n1) replace\n2) regex\n"))
        if n == 1:
            rep_old = input("Введите old:\n")
            rep_new = input("Введите new:\n")
        elif n == 2:
            reg_pattern = input("Введите pattern:\n")
            rep_replace = input("Введите replace:\n")
        else:
            print("Exit\n")
            exit()
    names = os.listdir(path_dir)
    for name in names:
        rename(path_dir, name, args.replace, args.regex)
