import os
import re
import shutil as sh
import subprocess


class Renamer:
    __regex: list
    __replace: list
    __source_path: str
    __destination_path: str
    __use_git_rename: bool

    def __init__(self, source_path=None, replace=None, regex=None, destination_path=None, use_git_rename=False):
        self.__zeros_name = set()
        self.__source_path = source_path
        self.__replace = replace
        self.__regex = regex
        if destination_path is None:
            self.__destination_path = self.__source_path
        else:
            self.__destination_path = destination_path
        if use_git_rename:
            def git_move(source_file, destination_file):
                os.chdir(os.path.dirname(source_file))
                try:
                    subprocess.check_call(["git", "mv", source_file, destination_file])
                except subprocess.CalledProcessError:
                    print("git not move: " + source_file + "->" + destination_file)

            self.rename_func = git_move
        else:
            self.rename_func = sh.move

    def __del__(self):
        self.clear_zeros()

    @property
    def replace(self):
        return self.__replace

    @replace.getter
    def replace(self):
        return self.__replace

    @replace.setter
    def replace(self, value):
        self.__replace = value

    @property
    def regex(self):
        return self.__regex

    @regex.getter
    def regex(self):
        return self.__regex

    @regex.setter
    def regex(self, value):
        self.__regex = value

    @property
    def source_path(self):
        return self.__source_path

    @source_path.getter
    def source_path(self):
        return self.__source_path

    @source_path.setter
    def source_path(self, value):
        self.__source_path = value

    @property
    def destination_path(self):
        return self.__destination_path

    @destination_path.getter
    def destination_path(self):
        return self.__destination_path

    @destination_path.setter
    def destination_path(self, value):
        self.__destination_path = value

    def get_new_name(self, name: str) -> str:
        new_name = name
        if self.__replace:
            new_name = name.replace(self.__replace[0], self.__replace[1])
        elif self.__regex:
            reg_compile = ""
            try:
                reg_compile = re.compile(self.__regex[0])
            except re.error:
                print("Regex error")
            new_name = re.sub(reg_compile, self.__regex[1], name)
        elif self.__destination_path:
            new_name = name
        return new_name

    def rename(self, name: str, new_name: str = None):
        if new_name is None:
            new_name = self.get_new_name(name)
            if self.__source_path is None or name == new_name and self.__source_path == self.__destination_path:
                print('skip:name= ' + name)
                return
        destination_path_new_name = os.path.join(self.__destination_path, new_name)
        source_path_name = os.path.join(self.__source_path, name)
        if os.path.exists(destination_path_new_name):
            i = 0
            while os.path.exists(destination_path_new_name):  # and new_name_ins != name:
                i += 1
                destination_path_new_name = os.path.join(self.__destination_path, Renamer.__new_name_ind(new_name, i))
            self.__zeros_name.add(destination_path_new_name)
        self.rename_func(source_path_name, destination_path_new_name)

    @staticmethod
    def __new_name_ind(old_name: str, ins: int) -> str:
        ins = ' ({})'.format(ins)
        name_ext = os.path.splitext(old_name)
        return str.join(ins, name_ext)

    def clear_zeros(self):
        back_up_source = self.__source_path
        back_up_new = self.__destination_path
        while self.__zeros_name:
            path_name = self.__zeros_name.pop()
            path = os.path.dirname(path_name)
            self.source_path = path
            self.destination_path = path
            name = os.path.basename(path_name)
            if os.path.exists(path_name):
                self.rename(name, self.__new_name_ind(name, 0))
            else:
                print("not found from [zeros_name]: " + path_name)
        self.source_path = back_up_source
        self.destination_path = back_up_new

    def destination_delete_object(self, name):
        if name in self.__zeros_name:
            self.__zeros_name.remove(name)
        path_name = os.path.join(self.__destination_path, name)
        if os.path.isfile(path_name):
            os.remove(path_name)
        elif os.path.isdir(path_name):
            os.rmdir(path_name)
            if path_name == self.__source_path:
                self.source_path = ''
