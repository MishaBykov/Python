import os
import re
import shutil as sh


class Renamer:

    def __init__(self, path, replace=None, regex=None, new_path=None):
        self.zeros_name = set()
        self.path = path
        self.replace = replace
        self.regex = regex
        if self.new_path is None:
            self.new_path = self.path
        else:
            self.new_path = new_path

    @staticmethod
    def __new_name_ind(old_name, ins):
        ins = '(' + str(ins) + ')'
        old_name = old_name.rsplit('.', 1)
        old_name[0] = old_name[0] + ' ' + ins
        return str.join('.', old_name)

    def __del__(self):
        for name in self.zeros_name:
            sh.move(os.path.join(self.new_path, name), os.path.join(self.new_path, Renamer.__new_name_ind(name, 0)))

    def rename(self, name):
        a = 0
        new_name = ''
        if self.replace:
            new_name = name.replace(self.replace[0], self.replace[1])
        elif self.regex:
            new_name = re.sub(self.regex[0], self.regex[1], name)
        elif self.new_path:
            new_name = name
            # [on_true] if [expression] else [on_false]
        if name == new_name:
            return
        path_new_name = os.path.join(self.new_path, new_name)
        exist_path = os.path.exists(path_new_name)
        if os.path.exists(exist_path):
            path_new_name_ins = os.path.join(self.new_path, (Renamer.__new_name_ind(new_name, a)))
            while os.path.exists(path_new_name_ins):
                a += 1
                path_new_name_ins = os.path.join(self.new_path, (Renamer.__new_name_ind(new_name, a)))
            self.zeros_name.add(path_new_name)
            sh.move(os.path.join(self.path, name), path_new_name_ins)
        else:
            sh.move(os.path.join(self.path, name), path_new_name)
