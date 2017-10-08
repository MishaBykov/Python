import argparse


def to_file(path_file):
    def next_str(file):
        global brackets_depth
        st = str(file.readline())
        brackets_depth += st.count("{") - st.count("}")

        return st

    def id_0(string):
        pass

    def id_1(string):
        if "namespace" in string:
            return 2
        elif "class" in string or "struct" in string:
            return 3
        elif "enum" in string:
            return 4
        elif "typedef" in string:
            return 5
        return 0

        # if not ("(" in string) or string.find("=") < string.find("("):
        #     return 6
        # return 0

    def id_2(string):
        if ";" in string:
            return 0

    def id_3(string):
        pass

    def id_4():
        pass

    def id_5(string):
        pass

    def id_6(string):
        pass

    brackets_depth = 0
    result = ""
    ns_path = []
    ns = ns_root
    funcs = [id_0, id_1, id_2, id_3, id_4, id_5]
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
    ns_root = [{}, [], 0]
    with open(source, 'r') as s:
        for line in s:
            to_file(line)
