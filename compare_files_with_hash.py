import argparse
import hashlib
import os

abs_path_file = os.path.join('D:/', 'video', 'One Piece', 'One Piece [1280x720]751+',
                             '751-One_Piece_TV_[Persona99](1280x720).rus.jap.mkv')


def get_dict_name_digest(path_dir: str, file_names: set[str]) -> dict:
    name_digest = {}
    os.chdir(path_dir)
    for file_name in file_names:
        hasher = hashlib.md5()
        with open(file_name, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
            digest = hasher.hexdigest()
            name_digest[file_name] = digest
    return name_digest


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

    name_digest_dict1 = get_dict_name_digest(dir1, common_file_names)
    name_digest_dict2 = get_dict_name_digest(dir2, common_file_names)

    for file_name in common_file_names:
        print(file_name + ': ', name_digest_dict1[file_name] == name_digest_dict2[file_name])
