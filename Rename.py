import os
import re
import shutil as sh


class Rename:
    __regex: list
    __replace: list
    __source_path: str
    __new_path: str

    def __init__(self, source_path=None, replace=None, regex=None, new_path=None):
        self.__zeros_name = set()
        self.__source_path = source_path
        self.__replace = replace
        self.__regex = regex
        if new_path is None:
            self.__new_path = self.__source_path
        else:
            self.__new_path = new_path

    def __del__(self):
        self.clear_zeros()

    @property
    def replace(self):
        return self.__replace

    @replace.setter
    def replace(self, value):
        self.__replace = value

    @property
    def regex(self):
        return self.__regex

    @regex.setter
    def regex(self, value):
        self.__regex = value

    @property
    def source_path(self):
        return self.__source_path

    @source_path.setter
    def source_path(self, value):
        self.__source_path = value

    @property
    def new_path(self):
        return self.__new_path

    @new_path.setter
    def new_path(self, value):
        self.__new_path = value

    def get_new_name(self, name: str) -> str:
        new_name = ''
        if self.__replace:
            new_name = name.replace(self.__replace[0], self.__replace[1])
        elif self.__regex:
            new_name = re.sub(self.__regex[0], self.__regex[1], name)
        elif self.__new_path:
            new_name = name
        return new_name

    def rename(self, name: str, new_name):
        new_path_new_name = os.path.join(self.__new_path, new_name)
        source_path_name = os.path.join(self.__source_path, name)
        if os.path.exists(new_path_new_name):
            new_name_ins = new_name
            a = 0
            while os.path.exists(os.path.join(self.__new_path, new_name_ins)):  # and new_name_ins != name:
                a += 1
                new_name_ins = Rename.__new_name_ind(new_name, a)
            self.__zeros_name.add(new_path_new_name)
            sh.move(source_path_name, os.path.join(self.__new_path, new_name_ins))
        else:
            sh.move(os.path.join(self.__source_path, name), new_path_new_name)

    def main(self, name: str):
        new_name = self.get_new_name(name)
        if self.__source_path is None or name == new_name and self.__source_path == self.__new_path:
            print('skip:name= ' + name)
            return
        self.rename(name, new_name)

    @staticmethod
    def __new_name_ind(old_name: str, ins: int) -> str:
        ins = ' ({})'.format(ins)
        name_ext = os.path.splitext(old_name)
        return str.join(ins, name_ext)

    def clear_zeros(self):
        back_up_source = self.__source_path
        back_up_new = self.__new_path
        while self.__zeros_name:
            path_name = self.__zeros_name.pop()
            path = os.path.dirname(path_name)
            self.source_path = path
            self.new_path = path
            name = os.path.basename(path_name)
            if os.path.exists(path_name):
                self.rename(name, self.__new_name_ind(name, 0))
            else:
                print("not found from [zeros_name]: " + path_name)
        self.source_path = back_up_source
        self.new_path = back_up_new

