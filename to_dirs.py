import argparse
from Rename import Rename
import os

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
    files_list = sorted(os.listdir(path), key=str.lower)
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
        rename = Rename(path, new_path=dir_name)
        for i in range(0, count_one_dir):
            try:
                rename.rename(files_list[ind_file])
            except IndexError:
                print(ind_file, count_files, len(files_list))
            ind_file += 1
            if ind_file == count_files:
                break
