import argparse
import codecs
import re


def for_file(path_file):
    global string

    def next_str():
        global brackets_depth, ns_path, string, ind_file
        string = str(array_file[ind_file]).split('//', maxsplit=1)
        string = string[0].replace('\r', '').replace('\n', '')
        ind_file += 1
        if ind_file == len_file:
            ind_file = -1
        if '/*' in string:
            to_end(['*/'])
        brackets_depth += string.count("{") - string.count("}")
        if ns_active[2] > brackets_depth:
            ns_path = ns_path[:-1]
            update_ns()
        return string

    def update_ns():
        global ns_active
        ns_active = ns_root
        for i in ns_path:
            ns_active = ns_active[0][i]

    def to_end(stop_words):
        global string
        strings = []
        while ind_file != -1:
            strings.append(string)
            for stop_word in stop_words:
                if stop_word in string:
                    return stop_word, strings
            string = next_str()

    def id_1():
        global string
        string = next_str()
        if "namespace " in string:
            return 2
        elif "class " in string or "struct " in string:
            return 3
        elif "enum " in string:
            return 4
        elif "typedef " in string:
            return 5
        return 1

    def id_2():
        global ns_active
        result = to_end([';', '{'])
        if result is None or result[0] == ';':
            return 1
        key = result[1][0].strip()
        if key not in ns_active[0]:
            ns_active[0][key] = [{}, [], brackets_depth]
        ns_active = ns_active[0][key]
        ns_path.append(key)
        return 1

    def id_3():
        result = to_end([';', '{', '<'])
        if result is None or result[0] == ';' or result[0] == '<':
            return 1
        to_save(3, result[1])
        return 1

    def id_4():
        result = to_end(['{'])
        if result is None:
            return 1
        to_save(4, result[1])
        return 1

    def id_5():
        result = to_end([';'])
        if result is None or ns_active[2] != brackets_depth:
            return 1
        to_save(5, result[1])
        return 1

    def to_save(type_string, st):
        if 3 == type_string:
            st = st[0].split(':')[0]
            st = re.sub(r" +", ' ', st)
            st = st.strip().split(sep=' ')
            if len(st) > 2:
                st.pop(1)
            st = ' '.join(st)
            ns_active[1].append(st + ';\n')
        elif 4 == type_string:
            st = st[0].replace('enum ', '').split(':')[0]
            st = re.sub(r" +", ' ', st)
            st = st.strip().split()
            if len(st) > 1:
                st.pop(0)
            st = ' '.join(st)
            ns_active[1].append("ENUM_DECL(" + st + ");\n")
        elif 5 == type_string:
            ns_active[1].append(st[0].strip() + '\n')
        return 1

    funcs = [0, id_1, id_2, id_3, id_4, id_5]
    with codecs.open(path_file.strip(), encoding='utf_8_sig', mode='r') as file:
        array_file = file.readlines()
        len_file = len(array_file)
        if len_file == 0:
            return
        string = next_str()
        state = 1
        while ind_file != -1:
            state = funcs[state]()


def print_ns(file, ns):
    for i in ns[0]:
        file.write(i + '\n{\n')
        print_ns(file, ns[0][i])
        file.write('}\n')
    for i in ns[1]:
        file.write(str(i))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='find forward')
    parser.add_argument("-pi", "--pathInput", nargs='?', type=str, help="input path dir")
    parser.add_argument("-po", "--pathOutput", nargs='?', type=str, help="output path")
    args = parser.parse_args()
    if args.pathInput is None:
        source = input("pathInput:\n")
    else:
        source = args.pathInput
    if args.pathOutput is None:
        out = input("pathOutput:\n")
    else:
        out = args.pathOutput
    ind_file = 0
    brackets_depth = 0
    ns_path = []
    ns_root = [{}, [], 0]
    ns_active = ns_root
    string = ""
    with open(source, 'r') as s:
        for line in s:
            for_file(line)
            ind_file = 0
            brackets_depth = 0
            ns_active = ns_root
            ns_path = []
    with open(out, 'w') as d:
        print_ns(d, ns_root)
