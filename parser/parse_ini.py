from typing import TextIO


class ParseIni:
    __generate_str: str
    __file: TextIO
    __groups: dict

    def __init__(self, file_name):
        self.__groups = {}
        self.__file = open(file_name)

    def generate_func(self):
        func_list = []

        def func_0(char: str):
            return func_1
        def func_1(char: str):
            pass
        def func_2(char: str):
            pass
        def func_3(char: str):
            pass
        def func_4(char: str):
            pass
        def func_5(char: str):
            pass
        def func_6(char: str):
            pass

        func_list = [func_0, func_1, func_2, func_3, func_4, func_5, func_6]


    def parse(self):
        # select_func = start_func
        funcs = []