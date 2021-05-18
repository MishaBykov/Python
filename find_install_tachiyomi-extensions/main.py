import argparse
import os
import shutil as sh
import subprocess
import json


class Tree:
    def __init__(self):
        self.root = {}

    def add(self, s: str):
        node = self.root
        for ch in s:
            if ch not in node:
                node[ch] = {}
            node = node[ch]

    def find(self, s: str) -> bool:
        node = self.root
        for ch in s:
            if ch not in node:
                return False
            node = node[ch]
        return True


def main(git_tach_ext: str, install_tach_ext: str, dest_copy_apk: str):
    name_files = []
    os.chdir(git_tach_ext)
    tree = Tree()
    with open(install_tach_ext) as file:
        for line in file:
            tree.add(line)

    subprocess.check_call(["git", "checkout", "repo"])
    file_path = "index.json"
    with open(file_path, "r") as file:
        os.chdir('apk')
        data = json.load(file)
        for object_json in data:
            if "name" in object_json and tree.find(object_json['name']):
                if 'apk' in object_json and os.path.exists(object_json['apk']):
                    sh.move(object_json['apk'], dest_copy_apk)
                else:
                    print("not found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-gte", "--git_tach_ext", type=str, help="git dir tachiyomi extensions")
    parser.add_argument("-da", "--dest_apk", type=str, help="dir ")
    parser.add_argument("-nite", "--name_install_tach_ext", type=str,
                        help="file with the names of installed extensions")
    args = parser.parse_args()

    main(args.git_tach_ext, args.name_install_tach_ext, args.name_install_tach_ext)
