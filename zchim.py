import os
import argparse


def new_name(old_name, ins):
    ins = '(' + str(ins) + ')'
    old_name = old_name.rsplit('.', 1)
    old_name[0] = old_name[0] + ' ' + ins
    return str.join('.', old_name)


def rename(path, name, replace, regex, a=0):
    nr = name.replace(src, rep_src)
    while True:
        try:
            os.rename(os.path.join(path, name),
                      os.path.join(path, nr if a == 0 else (new_name(nr, a))))
            break
        except FileExistsError:
            a += 1
        except OSError:
            break
    if a == 0:
        return None
    else:
        return path, nr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str,
                        help="input path dir")
    parser.add_argument("-rp", "--replace", nargs=2,
                        help="input source")
    parser.add_argument("-rg", "--regex", nargs=2,
                        help="input replace")
    args = parser.parse_args()
    path_dir = args.path
    if args.regex is None and args.replace is None:
        a = input("Введите номер:\n1) replace\n2) regex\n")
        if a == 1:

    #     source = input("Введите часть имени: ")
    # else:
    #     source = args.source
    # if args.replace is None:
    #     rep = input("Введите замену части имени: ")
    # else:
    #     rep = args.rep
    names = os.listdir(path_dir)
    zeros = set()
    for name in names:
        zeros.add(rename(path_dir, name, source, rep))
    if None in zeros:
        zeros.remove(None)
    for zero in zeros:
        try:
            os.rename(os.path.join(zero[0], zero[1]), os.path.join(zero[0], new_name(zero[1], 0)))
        except OSError:
            rename(zero[0], zero[1], "", "", a=1)
