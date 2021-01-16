import argparse
import os
from rename.Renamer import Renamer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Name part replacement')
    parser.add_argument("path", type=str, help="input path dir")
    parser.add_argument("-g", "--git", action='store_true')
    parser.add_argument("-rp", "--replace", nargs=2,
                        help="input source")
    parser.add_argument("-rg", "--regex", nargs=2,
                        help="input replace")
    args = parser.parse_args()
    path_dir = args.path
    flag_from_keyboard = args.regex is None and args.replace is None
    if flag_from_keyboard:
        n = input("Введите номер:\n1) replace\n2) regex\nOther Exit\n")
        if n == '1':
            args.replace = [input("Введите old:\n"), input("Введите new:\n")]
            print(args.replace)
        elif n == '2':
            args.regex = [input("Введите pattern:\n"), input("Введите replace:\n")]
            print(args.regex)
        else:
            print("Exit\n")
            exit()
        input()
    renamer = Renamer(path_dir, args.replace, args.regex, use_git_rename=args.git)
    for name in os.listdir(path_dir):
        renamer.rename(name)
