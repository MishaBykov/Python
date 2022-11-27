import json

json_path = dict()


def add_path(value, deap: int):
    if deap not in json_path:
        json_path[deap] = []
    json_path[deap].append(value)


def find_key(root: any, key_find: str, deap=0) -> bool:
    if type(root) == list:
        return find_key_in_array(root, key_find, deap)
    if type(root) == dict:
        return find_key_in_object(root, key_find, deap)


def find_key_in_array(root: list, key_find: str, deap: int) -> bool:
    result = False
    for i in range(len(root)):
        if find_key(root[i], key_find, deap + 1):
            add_path(i, deap)
            result = True
    return result


def find_key_in_object(root: dict, key_find: str, deap: int) -> bool:
    result = False
    if key_find in root.keys():
        result = True
    for key in root.keys():
        if find_key(root[key], key_find, deap + 1):
            add_path(key, deap)
            result = True
    return result


if __name__ == '__main__':
    id = 'comkdlimbkhemidbbpchhepidbmjpnhh'
    path_file = '/home/misha/.config/yandex-browser/Default/Preferences'

    with open(path_file) as file:
        data = json.load(file)

    find_key(data, id)
    print(sorted(json_path.items()))
