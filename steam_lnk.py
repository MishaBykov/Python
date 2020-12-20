import os

paths = {
    "icon_dirs": r"test_icon",
    "app_manifests": r"D:\FilesGames\SteamLib\steamapps",
    "install_games": r"D:\FilesGames\SteamLib\steamapps\common"
}


def list_icons_data(path_dir_icons: str) -> dict:
    result = {}
    for file in os.scandir(path_dir_icons):
        file: os.DirEntry
        if file.name.rsplit(os.path.extsep, 1)[-1] == "url":
            data_icon = parse_data_icon(file.path)
            if data_icon['InternetShortcut']["URL"].split(':')[0] == "steam":
                game_id = data_icon['InternetShortcut']["URL"].rsplit('/', 1)[-1]
                result[game_id] = data_icon
    return result


def parse_data_icon(path_icon: str) -> dict:
    result = {}
    key_root = ''
    if os.path.exists(path_icon):
        result["path_icon"] = path_icon
        with open(path_icon) as file_ico:
            for string in file_ico:
                string = string.strip()
                if '=' in string and key_root:
                    key, value = string.split('=', 1)
                    result[key_root][key] = value
                if string[0] == '[':
                    key_root = string[string.find('[') + 1:string.find(']')]
                    result[key_root] = {}
    return result


def write_data_icon(data_icon: dict, path_icon: str):
    strings = []
    for key1 in data_icon:
        if key1 == "path_icon":
            continue
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


def get_app_manifests(path_manifests: str) -> dict:
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
    icons_data = list_icons_data(paths["icon_dirs"])
    app_manifests_data = get_app_manifests(paths["app_manifests"])
    for game_id in icons_data.keys():
        install_dir = app_manifests_data[game_id]["AppState"]["installdir"]
        path_fist_exe = find_fist_exe(os.path.join(paths["install_games"], install_dir))
        icons_data[game_id]["InternetShortcut"]["IconFile"] = path_fist_exe
        if icons_data[game_id]["InternetShortcut"]["IconIndex"] != '0':
            icons_data[game_id]["InternetShortcut"]["IconIndex"] = '0'
        write_data_icon(icons_data[game_id], icons_data[game_id]["path_icon"])


if __name__ == '__main__':
    main()
