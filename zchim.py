import argparse
import os
import rename as r

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
        r.rename(path_dir, name, args.replace, args.regex)
