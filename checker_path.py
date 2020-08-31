import os

path_ini = r"D:\_Work\Clients\Pyatigorsk\PyatigorskTeploService\Stack.Srv\Bin\0\STACK.INI"
os.chdir(r"D:\_Work\Clients\Pyatigorsk\PyatigorskTeploService\Stack.Srv\Bin\0")

with open(path_ini, 'r', encoding='utf-8') as file:
    for line in file:
        if line == '\n' or '#' in line or line[0] == '[':
            continue
        path = line.split('=', 1)[-1].replace('\n', '')
        if not os.path.exists(path):
            print('!' + path)
