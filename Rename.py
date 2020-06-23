import os
import re
import shutil as sh


class Rename:
    def __init__(self, path, replace=None, regex=None, new_path=None):
        self.zeros_name = set()
        self.path = path
        self.replace = replace
        self.regex = regex
        if new_path is None:
            self.new_path = self.path
        else:
            self.new_path = new_path

    def __del__(self):
        while self.zeros_name:
            name = self.zeros_name.pop()
            if os.path.exists(os.path.join(self.new_path, name)):
                self.rename(os.path.join(self.new_path, name),
                            os.path.join(self.new_path, Rename.__new_name_ind(name, 0)))
            else:
                print("not found from [zeros_name]: " + os.path.join(self.new_path, name))

    def get_new_name(self, name: str) -> str:
        new_name = ''
        if self.replace:
            new_name = name.replace(self.replace[0], self.replace[1])
        elif self.regex:
            new_name = re.sub(self.regex[0], self.regex[1], name)
        elif self.new_path:
            new_name = name
        return new_name

    def rename(self, name: str, new_name):
        if os.path.exists(os.path.join(self.new_path, new_name)):
            new_name_ins = new_name
            # todo что здесь происходит?
            a = 0
            while os.path.exists(os.path.join(self.new_path, new_name_ins)):  # and new_name_ins != name:
                a += 1
                new_name_ins = Rename.__new_name_ind(new_name, a)
            self.zeros_name.add(new_name)
            sh.move(os.path.join(self.path, name), os.path.join(self.new_path, new_name_ins))
        else:
            sh.move(os.path.join(self.path, name), os.path.join(self.new_path, new_name))

    def main(self, name: str):
        new_name = self.get_new_name(name)
        if name == new_name and self.path == self.new_path:
            return
        self.rename(name, new_name)

    @staticmethod
    def __new_name_ind(old_name: str, ins: int) -> str:
        ins = ' ({})'.format(ins)
        name_ext = os.path.splitext(old_name)
        return str.join(ins, name_ext)
