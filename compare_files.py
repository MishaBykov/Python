import argparse
import filecmp
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare files with the same name using a hash')
    parser.add_argument("dir1", type=str, help="path dir1")
    parser.add_argument("dir2", type=str, help="path dir2")
    args = parser.parse_args()

    dir1: str = args.dir1
    dir2: str = args.dir2

    file_names1 = set(os.listdir(dir1))
    file_names2 = set(os.listdir(dir2))

    common_file_names = file_names1.intersection(file_names2)

    count_files = len(common_file_names)
    print('total files:', count_files)
    for file_name in common_file_names:
        cmp_result = filecmp.cmp(os.path.join(dir1, file_name), os.path.join(dir2, file_name))
        if not cmp_result:
            print(file_name + ':', cmp_result)
        print('files left:', --count_files)
