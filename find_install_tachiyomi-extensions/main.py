import os
import subprocess
import json

path_git_temp_tach_ext = r"/home/misha/repos/tachiyomi-extensions"
path_name_tach_ext = "/home/misha/PycharmProjects/Python/find_install_tachiyomi-extensions/_name_tachiyomi-extensions.txt"
# appName : "Tachiyomi: $extName",
prefixAppName = "Tachiyomi: "
# setProperty("archivesBaseName", "tachiyomi-$pkgNameSuffix-v$versionName")
prefixFileName = "tachiyomi-"

example_app_name = "Tachiyomi: Bato.to  1.2.7"


class Tree:
    def __init__(self):
        self.root = {}
        self.all_str = []

    def add(self, s: str):
        self.all_str.append(s)
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
        for i in range(len(self.all_str) - 1, -1, -1):
            if s in self.all_str[i]:
                self.all_str.pop(i)
        return True


name_files = []
os.chdir(path_git_temp_tach_ext)
tree = Tree()
with open(path_name_tach_ext) as file:
    for line in file:
        tree.add(line)

subprocess.check_call(["git", "checkout", "repo"])
file_path = "index.json"
min_file_path = "index.min.json"
with open(file_path, "r") as file:
    data = json.load(file)
    for object_json in data:
        if "name" in object_json and tree.find(object_json['name']):
            name_files.append(object_json['apk'])

os.chdir('apk')
print("count files " + str(len(name_files)))
for file in name_files:
    if os.path.exists(file):
        print('ok ' + file)
    else:
        print("no " + file)
for i in tree.all_str:
    print(i)
