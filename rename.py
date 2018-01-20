import os
import re


def __new_name(old_name, ins):
    ins = '(' + str(ins) + ')'
    old_name = old_name.rsplit('.', 1)
    old_name[0] = old_name[0] + ' ' + ins
    return str.join('.', old_name)


def rename(path, name, replace=None, regex=None, new_path=None):
    if new_path is None:
        new_path = path
    a = 0
    nn = ''
    if replace:
        nn = name.replace(replace[0], replace[1])
    elif regex:
        nn = re.sub(regex[0], regex[1], name)
    else:
        nn = name
    while True:
        try:
            os.rename(os.path.join(path, name), os.path.join(new_path, (__new_name(nn, a))))
            break
        except FileExistsError:
            a += 1
        except OSError:
            return
    if a == 0:
        try:
            os.rename(os.path.join(new_path, (__new_name(nn, a))), os.path.join(new_path, nn))
        except FileExistsError:
            rename(path, nn, replace, regex, new_path)
