import os
import shutil as sh

path = r"F:\Games"
find_dir = ".egstore"
os.chdir(path)
for i in os.scandir(path):
    i: os.DirEntry
    if i.is_dir() and os.path.exists(os.path.join(i.path, find_dir)):
        sh.move(i.path, os.path.join(path, 'egs'))

