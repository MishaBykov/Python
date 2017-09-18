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

    def i_d_2():
        pass

    def i_d_3():
        pass

    def i_d_4():
        pass

    def i_d_5():
        pass


    brackets_depth = 0
    i_d = 0
    active_string = ""
    with open(path_file, 'r') as p_f:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace of part of a name')
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
