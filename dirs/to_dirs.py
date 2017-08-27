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
    except:
        f(files, count_one_dir, name_dir, shift_name, length_name + 1)


path = input("Введите путь каталога: ")
countOneDir = int(input("Количество файлов на одну папку: "))
shiftName = int(input("name_start: "))
files_list = sorted(os.listdir(path), key=sort_alphabet)
os.chdir(path)
lengthName = int(len(str(len(files_list) // countOneDir + shiftName)))
nameDir = 0
f(files_list, countOneDir, nameDir, shiftName, lengthName)
