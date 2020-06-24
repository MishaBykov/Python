import argparse
import os
import zipfile

spaces = "    "

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='from dir dirs to zip')
    parser.add_argument("source_path_dir", type=str, help="source path dir")
    parser.add_argument("destination_path_dir", type=str, help="destination path dir")
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
                if os.path.exists(zip_name):
                    os.remove(zip_name)
                print(spaces + "exist destination")
                continue
            temp_path_zip = os.path.join(destination, "temp.zip")
            print(spaces + "create zip")
            z = zipfile.ZipFile(temp_path_zip, 'w')  # Создание нового архива
            print(spaces + "fill zip")
            for root, dirs, files in os.walk(d.path):  # Список всех файлов и папок в директории folder
                for file in files:
                    z.write(os.path.join(root, file))  # Создание относительных путей и запись файлов в архив
            z.close()
            print(spaces + "rename")
            os.rename(temp_path_zip, path_destination_zip)

