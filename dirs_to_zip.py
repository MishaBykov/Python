import argparse
import os
import shutil
import zipfile

# todo добавить логирование
spaces = "    "
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='from dir dirs to zip')
    parser.add_argument("source", type=str, help="source path dir")
    parser.add_argument("destination", type=str, help="destination path dir")
    parser.add_argument("-m", "--move", action='store_true', help="delete source")
    args = parser.parse_args()

    source = args.source
    if not os.path.exists(source):
        print("source dir not exist")
        exit()
    destination = args.destination
    if not os.path.exists(destination):
        print("create destination dir")
        os.mkdir(destination)

    os.chdir(source)
    for dir_entry in os.scandir():
        dir_entry: os.DirEntry
        if dir_entry.is_dir():
            print(dir_entry.name)
            path_destination_zip = os.path.join(destination, dir_entry.name + '.zip')
            path_zip_temp = os.path.join(destination, path_destination_zip + ".temp")
            # print(spaces + "create zip")
            zf = zipfile.ZipFile(path_zip_temp, 'w')  # Создание нового архива
            # print(spaces + "fill zip")
            for root, dirs, files in os.walk(dir_entry.path):  # Список всех файлов и папок в директории folder
                for file in files:
                    zf.write(os.path.join(root, file))  # Создание относительных путей и запись файлов в архив
            zf.close()
            # print(spaces + "rename")
            os.rename(path_zip_temp, path_destination_zip)
            if args.move:
                shutil.rmtree(dir_entry)
        if dir_entry.is_file():
            with zipfile.ZipFile(os.path.join(destination, "root.zip"), 'a') as zf:
                zf.write(dir_entry.name)
                os.remove(dir_entry)
    if args.move and not os.listdir(source):
        os.chdir("..")
        os.rmdir(source)
