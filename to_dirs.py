import argparse
import shutil as sh
import Renamer as rn
import os


def sort_alphabet(input_str):
    return str(input_str)[0].lower()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
    parser.add_argument("path", type=str,
                        help="input path dir")
    parser.add_argument("-cod", "--count_one_dir", nargs='?',
                        help="input countOneDir ")
    args = parser.parse_args()
    path = args.path
    if args.count_one_dir is None:
        count_one_dir = input("Количество файлов на одну папку: ")
    else:
        count_one_dir = args.count_one_dir
    count_one_dir = int(count_one_dir)
    files_list = sorted(os.listdir(path), key=sort_alphabet)
    count_files = len(files_list)
    os.chdir(path)
    count_new_dir = count_files // count_one_dir + 1
    length_name = int(len(str(count_new_dir)))
    ind_file = 0
    for dir_name in range(1, count_new_dir + 1):
        dir_name = '0' * (length_name - len(str(dir_name))) + str(dir_name)
        while os.path.exists(dir_name):
            dir_name = '0' + dir_name
        os.mkdir(dir_name)
        for i in range(0, count_one_dir):
            rn.rename(path, files_list[ind_file], new_path=dir_name)
            ind_file += 1
            if ind_file == count_files:
                break
