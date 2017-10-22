import argparse


def to_file(path_file):
    def next_str(file):
        global brackets_depth, ns_path
        st = str(file.readline())
        brackets_depth += st.count("{") - st.count("}")
        if ns[2] > brackets_depth:
            ns_path = ns_path[:-1]
            update_ns()
        return st

    def update_ns():
        global ns
        ns = ns_root
        for i in ns_path:
            ns = ns[0][i]

    def to_end(file, string, stop_words):
        strings = [string]
        while True:
            strings.append(string)
            for stop_word in stop_words:
                if stop_word in string:
                    return stop_word, strings
            string = next_str(file)

    def id_1(string, file):
        if "namespace" in string:
            return 2
        elif "class" in string or "struct" in string:
            return 3
        elif "enum" in string:
            return 4
        elif "typedef" in string:
            return 5
        return 0

    def id_2(string, file):
        global ns
        result = to_end(file, string, [';', '{'])
        if result[0] == ';':
            return 1
        ns[0][string] = [{}, [], brackets_depth]
        ns_path.append(string)
        ns = ns[0][string]
        return 0

    def id_3(string, file):
        result = to_end(file, string, [';', '{'])
        if result[0] == ';':
            return 1
        to_save(3, result[1])
        return 0

    def id_4(string, file):
        result = to_end(file, string, ['{'])
        to_save(4, result[1])
        return 0

    def id_5(string, file):
        result = to_end(file, string, [';'])
        to_save(5, result[1])
        return 0

    def to_save(type_string, string):
        if 3 == type_string:
            ns[1].append(string)
        elif 4 == type_string:
            ns[1].append("ENUM_DECL(" + string[:-1] + ")\n")
        elif 5 in string:
            ns[1].append(string)
        return 1

    brackets_depth = 0
    ns_path = []
    ns = ns_root
    state = 0
    funcs = [0, id_1, id_2, id_3, id_4, id_5]
    with open(path_file, 'r') as i_f:
        if 0 == state:
            state = 1




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
    pass
    fOut.close()