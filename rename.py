import os
import re
import shutil as sh


def __new_name(old_name, ins):
    ins = '(' + str(ins) + ')'
    old_name = old_name.rsplit('.', 1)
    old_name[0] = old_name[0] + ' ' + ins
    return str.join('.', old_name)


def rename(path, name, replace=None, regex=None, new_path=None):
    if new_path is None:
        new_path = path
    a = 0
    # new_name = ''
    if replace:
        new_name = name.replace(replace[0], replace[1])
    elif regex:
        new_name = re.sub(regex[0], regex[1], name)
    else:
        return
        # [on_true] if [expression] else [on_false]
    if os.path.join(path, name) == os.path.join(new_path, new_name):
        return
    new_name_ins = os.path.join(new_path, (__new_name(new_name, a)) if a > 0 else new_name)
    while os.path.exists(new_name_ins):
        a += 1
        new_name_ins = os.path.join(new_path, (__new_name(new_name, a)) if a > 0 else new_name)
    sh.move(os.path.join(path, name), new_name_ins)
    if a != 0:
        sh.move(os.path.join(new_path, new_name), os.path.join(new_path, __new_name(new_name, 0)))
