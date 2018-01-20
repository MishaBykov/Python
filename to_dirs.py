import argparse
import shutil as sh
import os


def new_name(old_name, shift_name, length_name):
    return ((length_name - len(str(old_name + shift_name))) * "0") + str(old_name + shift_name)


def sort_alphabet(input_str):
    return str(input_str)[0].lower()


def f(files, count_one_dir, name_dir, shift_name, length_name):
    try:
        for i in range(len(files) // count_one_dir + (0 if 0 == len(files) % count_one_dir else 1)):
            name = new_name(name_dir, shift_name, length_name)
            os.mkdir(path + '\\' + name)
            for file in files[i * count_one_dir:(i + 1) * count_one_dir]:
                sh.move(path + '\\' + file, path + '\\' + name)
            name_dir += 1
    except sh.Error:
        f(files, count_one_dir, name_dir, shift_name, length_name + 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str,
                        help="input path dir")
    parser.add_argument("-ns", "--nameStart", nargs='?',
                        help="input nameStart")
    parser.add_argument("-cod", "--countOneDir", nargs='?',
                        help="input countOneDir ")
    args = parser.parse_args()
    path = args.path
    countOneDir = args.countOneDir
    if countOneDir is None:
        countOneDir = int(input("Количество файлов на одну папку: "))
    nameStart = args.nameStart
    if nameStart is None:
        nameStart = int(input("nameStart: "))
    shiftName = nameStart

    files_list = sorted(os.listdir(path), key=sort_alphabet)
    os.chdir(path)
    lengthName = int(len(str(len(files_list) // countOneDir + shiftName)))
    nameDir = 0
    f(files_list, countOneDir, nameDir, shiftName, lengthName)
