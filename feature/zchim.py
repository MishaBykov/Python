import os


def new_name(old_name, ins):
    ins = '(' + str(ins) + ')'
    old_name = old_name.rsplit('.', 1)
    old_name[0] = old_name[0] + ' ' + ins
    return str.join('.', old_name)


def rename(path, name, src, rep_src, a=0):
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


def main():
    path_dir = input("Введите путь каталога: ")
    source = input("Введите часть имени: ")
    rep = input("Введите замену части имени: ")
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


if __name__ == '__main__':
    main()
