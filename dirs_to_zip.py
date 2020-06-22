import os
import zipfile

spaces = "    "

# todo source path to params
os.chdir(r'')
dirs = os.scandir()

# todo destination path to params
destination = r''

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
        z.namelist()
        print(spaces + "fill zip")
        for root, dirs, files in os.walk(d.path):  # Список всех файлов и папок в директории folder
            for file in files:
                z.write(os.path.join(root, file))  # Создание относительных путей и запись файлов в архив
        z.close()
        print(spaces + "rename")
        os.rename(temp_path_zip, path_destination_zip)

