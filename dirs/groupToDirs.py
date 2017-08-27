import os


def f(path_dir):
    i = 0
    while True:
        files = os.listdir(path)
        while i < len(files):
            name = files[i].split(sep=" (")
            name.sort(reverse=True)
            if len(name) > 1:
                name = name[0]
                os.mkdir(name)
                os.system('move "*' + name + '*" "' + name + '"')
                break
            i += 1
        if i == len(files):
            break


path = input("Путь: ")
os.system('cd /d  path')
os.chdir(path)
f(path)
