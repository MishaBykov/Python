import argparse
import os
from Rename import Rename

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Name part replacement')
    parser.add_argument("path", type=str, help="input path dir")
    parser.add_argument("-rp", "--replace", nargs=2,
                        help="input source")
    parser.add_argument("-rg", "--regex", nargs=2,
                        help="input replace")
    args = parser.parse_args()
    path_dir = args.path
    if args.regex is not None and args.replace is not None:
        n = input("Введите номер:\n1) replace\n2) regex\nOther Exit\n")
        if n == '1':
            args.regex = None
        elif n == '2':
            args.replace = None
        else:
            print("Exit\n")
            exit()
    if args.regex is None and args.replace is None:
        n = input("Введите номер:\n1) replace\n2) regex\nOther Exit\n")
        if n == '1':
            args.replace = []
            args.replace.append(input("Введите old:\n"))
            args.replace.append(input("Введите new:\n"))
            print(args.replace)
            input()
        elif n == '2':
            args.regex = []
            args.regex.append(input("Введите pattern:\n"))
            args.regex.append(input("Введите replace:\n"))
            print(args.regex)
            input()
        else:
            print("Exit\n")
            exit()
    rename = Rename(path_dir, args.replace, args.regex)
    for name in os.listdir(path_dir):
        rename.main(name)
