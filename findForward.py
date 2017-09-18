import argparse


def to_file(path_file):
    def i_d_0(string):
        if "const" in string:
            return 1
        if "class" in string or "struct" in string:
            return 2
        if "typedef" in string:
            return 3

    def i_d_1(string):
        if not ("(" in string) or string.find("=") < string.find("("):
            return 6
        return 0

    def i_d_2(string):
        if ";" in string:
            return 0

    def i_d_3(string):
        pass

    def i_d_4():
        pass

    def i_d_5(string):
        pass

    def i_d_6(string):
        pass

    brackets_depth = 0
    i_d = 0
    active_string = ""
    path_ns = ""
    funcs = [i_d_0, i_d_1, i_d_2, i_d_3, i_d_4, i_d_5]
    with open(path_file, 'r') as o_f:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='find forward')
    parser.add_argument("pathInput", type=str,
                        help="input path dir")
    parser.add_argument("pathOutput", type=str,
                        help="output path")
    args = parser.parse_args()
    source = args.pathInput
    out = args.pathOutput
    fOut = open(out, 'a')
    ns = [{}, []]
    with open(source, 'r') as s:
        for line in s:
            to_file(line)
