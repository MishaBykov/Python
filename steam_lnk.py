import os

paths = {
    "icon_test": r"test_icon\Aragami.url",
    "exe_test": r"D:\FilesGames\SteamLib\steamapps\common\BloodCard\BloodCard.exe",

    "icon_dirs": r"test_icon",
    "app_manifests": r"D:\FilesGames\SteamLib\steamapps",
    "install_games": r"D:\FilesGames\SteamLib\steamapps\common"
}


def parse_data_icon(path_icon: str) -> dict:
    result = {}
    key_root = ''
    with open(path_icon) as file_ico:
        for string in file_ico:
            string = string.strip()
            if '=' in string and key_root:
                key, value = string.split('=')
                result[key_root][key] = value
            if string[0] == '[':
                key_root = string[string.find('[') + 1:string.find(']')]
                result[key_root] = {}
    return result


def write_data_icon(data_icon: dict, path_icon: str):
    strings = []
    for key1 in data_icon:
        strings.append('[' + key1 + ']')
        for key2 in data_icon[key1]:
            strings.append(key2 + '=' + data_icon[key1][key2])
    with open(path_icon, 'w') as ico:
        ico.write('\n'.join(strings))


def parse_app_manifest(path_manifest: str) -> dict:
    result = {}
    key_path = []
    with open(path_manifest) as file:
        current_dict = result
        for string in file:
            string = string.replace('"', '').split()
            split_len = len(string)
            if split_len == 1:
                if string[0] == '}':
                    key_path.pop()
                    current_dict = result
                    for key in key_path:
                        current_dict = current_dict[key]
                elif string[0] == '{':
                    current_dict[key_path[-1]] = {}
                    current_dict = current_dict[key_path[-1]]
                else:
                    key_path.append(string[0])
            elif split_len == 2:
                current_dict[string[0]] = string[1]

    return result


def get_dict_app_manifests(path_manifests: str) -> dict:
    result = {}
    for de in os.scandir(path_manifests):
        de: os.DirEntry
        if de.is_file() and de.name.rsplit('.', 1) == "acf":
            data_manifest = parse_app_manifest(de.path)
            result[data_manifest["appid"]] = data_manifest
    return result


def find_fist_exe(path_dir: str) -> str:
    result = ''
    for de in os.scandir(path_dir):
        de: os.DirEntry
        if result:
            break
        if de.is_dir():
            result = find_fist_exe(de.path)
        elif de.is_file() and de.name.rsplit('.', 1)[-1] == "exe":
            result = de.path
        else:
            pass
    return result


def main():
    data_icon = parse_data_icon(paths["icon_test"])
    data_icon['InternetShortcut']['IconFile'] = paths["exe_test"]
    write_data_icon(data_icon, paths["icon_test"])
    r = parse_app_manifest(r"D:\FilesGames\SteamLib\steamapps\appmanifest_3720.acf")
    path_exe = find_fist_exe(paths["install_games"])

if __name__ == '__main__':
    main()
