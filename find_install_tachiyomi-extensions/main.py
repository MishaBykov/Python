import os
import subprocess

path_git_temp_tach_ext = r"/home/misha/repos/tachiyomi-extensions"
path_name_tach_ext = "/home/misha/PycharmProjects/Python/find_install_tachiyomi-extensions/_name_tachiyomi-extensions.txt"
# appName : "Tachiyomi: $extName",
prefixAppName = "Tachiyomi: "
# setProperty("archivesBaseName", "tachiyomi-$pkgNameSuffix-v$versionName")
prefixFileName = "tachiyomi-"

example_app_name = "Tachiyomi: Bato.to  1.2.7"


# versionName "$libVersion.$extVersionCode"

# ext {
#     extName = 'Bato.to'
#     pkgNameSuffix = 'all.batoto'
#     extClass = '.BatoToFactory'
#     extVersionCode = 9
#     libVersion = '1.2'
#     containsNsfw = true
# }
#  обойти build.gradle

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

if not os.path.exists("src"):
    subprocess.check_call(["git", "checkout", "master"])
for root, dirs, files in os.walk("src"):
    for file in files:
        if file != "build.gradle":
            continue
        with open(os.path.join(root, file)) as open_file:
            variables = {}
            for line in open_file:
                if '=' not in line:
                    continue
                name, value = line.split('=', maxsplit=1)
                name = name.strip()
                value = value.strip().strip("'").strip('"')
                variables[name] = value
            if "extName" in variables:
                if tree.find(prefixAppName + variables['extName']):
                    name_files.append(prefixFileName + variables['pkgNameSuffix']
                                      + '-v' + variables['libVersion'] + '.' + variables['extVersionCode'] + '.apk')
# subprocess.check_call(["git", "checkout", "repo"])
# os.chdir('apk')
# print("count files " + str(len(name_files)))
# for file in name_files:
#     if os.path.exists(file):
#         print('ok ' + file)
#     else:
#         print("no " + file)
for i in tree.all_str:
    print(i)

