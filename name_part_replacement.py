import argparse
import os
from rename.Renamer import Renamer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Name part replacement', prefix_chars='/')
    parser.add_argument("/p", "//path", type=str, help="input path")
    parser.add_argument("/r", "//revert", action='store_true')
    parser.add_argument("/g", "//git", action='store_true')
    parser.add_argument("/s", "//session", action='store_true')
    parser.add_argument("/rp", "//replace", nargs=2,
                        help="input source")
    parser.add_argument("/rg", "//regex", nargs=2,
                        help="input replace")
    args = parser.parse_args()
    path_dir = args.path
    if args.revert:
        Renamer.revert_last_state_file()
        exit()
    renamer = None
    while True:
        flag_from_keyboard = args.regex is None and args.replace is None
        if flag_from_keyboard:
            n = input("Введите номер:\n1) replace\n2) regex\n3) Отктить последнее изменение\nOther Exit\n")
            if n == '1':
                args.replace = [input("Введите old:\n"), input("Введите new:\n")]
                print(args.replace)
            elif n == '2':
                args.regex = [input("Введите pattern:\n"), input("Введите replace:\n")]
                print(args.regex)
            elif n == '3':
                if renamer is None:
                    Renamer.revert_last_state_file()
                    continue
                else:
                    renamer.revert_last_state()
            else:
                print("Exit\n")
                if renamer is not None:
                    del renamer
                break
            input()
        if renamer is None:
            renamer = Renamer(path_dir, args.replace, args.regex, use_git_mv=args.git, save_state=True)
        else:
            renamer.replace = args.replace
            renamer.regex = args.regex
        renamer.rename_mass()
        if not args.session:
            break
        else:
            args.regex = None
            args.replace = None
