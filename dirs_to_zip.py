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

    if not os.path.exists(args.source):
        print("source dir not exist")
        exit()
    os.chdir(args.source)
    destination = args.destination
    if not os.path.exists(destination):
        print("create destination dir")
        os.mkdir(destination)

    for d in os.scandir():
        d: os.DirEntry
        if d.is_dir():
            print(d.name)
            zip_name = d.name + '.zip'
            path_destination_zip = os.path.join(destination, zip_name)
            if os.path.exists(path_destination_zip):
                # print(spaces + "exist destination")
                continue
            temp_path_zip = os.path.join(destination, path_destination_zip + ".temp")
            if os.path.exists(temp_path_zip):
                os.remove(temp_path_zip)
            # print(spaces + "create zip")
            z = zipfile.ZipFile(temp_path_zip, 'w')  # Создание нового архива
            # print(spaces + "fill zip")
            for root, dirs, files in os.walk(d.path):  # Список всех файлов и папок в директории folder
                for file in files:
                    full_path = os.path.join(root, file)
                    z.write(full_path)  # Создание относительных путей и запись файлов в архив
            z.close()
            # print(spaces + "rename")
            os.rename(temp_path_zip, path_destination_zip)
            if args.move:
                shutil.rmtree(d)
    shutil.rmtree(args.source)
