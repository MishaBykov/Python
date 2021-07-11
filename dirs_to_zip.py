import argparse
import os
import shutil
import zipfile

# todo добавить логирование
spaces = "    "
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='from dir dirs to zip')
    parser.add_argument("source_path_dir", type=str, help="source path dir")
    parser.add_argument("destination_path_dir", type=str, help="destination path dir")
    parser.add_argument("-m", "--move", action='store_true', help="delete source")
    args = parser.parse_args()

    os.chdir(args.source_path_dir)
    dirs = os.scandir()

    destination = args.destination_path_dir

    for d in dirs:
        d: os.DirEntry
        if d.is_dir():
            print(d.name)
            zip_name = d.name + '.zip'
            path_destination_zip = os.path.join(destination, zip_name)
            if os.path.exists(path_destination_zip):
                # print(spaces + "exist destination")
                continue
            temp_path_zip = os.path.join(destination, path_destination_zip + ".temp")
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
