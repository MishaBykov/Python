import os
import re
import shutil as sh


class Renamer:

    def __init__(self, path, replace=None, regex=None, new_path=None):
        self.zeros_name = set()
        self.path = path
        self.replace = replace
        self.regex = regex
        if new_path is None:
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
            if os.path.join(self.new_path, name):
                sh.move(os.path.join(self.new_path, name), os.path.join(self.new_path, Renamer.__new_name_ind(name, 0)))
            else:
                print("not found from [zeros_name]: " + os.path.join(self.new_path, name))

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
        if os.path.exists(os.path.join(self.new_path, new_name)):
            new_name_ins = new_name
            while os.path.exists(os.path.join(self.new_path, new_name_ins)) and new_name_ins != name:
                a += 1
                new_name_ins = Renamer.__new_name_ind(new_name, a)
            self.zeros_name.add(new_name)
            sh.move(os.path.join(self.path, name), os.path.join(self.new_path, new_name_ins))
        else:
            sh.move(os.path.join(self.path, name), os.path.join(self.new_path, new_name))
