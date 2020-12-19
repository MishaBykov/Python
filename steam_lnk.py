import os

path_dir = r"test"
path_ico = r"test\Aragami.url"
path_exe = r"D:\FilesGames\SteamLib\steamapps\common\BloodCard\BloodCard.exe"


def parse_data_icon(path: str) -> dict:
    result = {}
    key_root = ''
    with open(path_ico) as file_ico:
        for string in file_ico:
            string = string.strip()
            if '=' in string and key_root:
                key, value = string.split('=')
                result[key_root][key] = value
            if string[0] == '[':
                key_root = string[string.find('[') + 1:string.find(']')]
                result[key_root] = {}
    return result


def data_icon_to_strings(data_icon: dict, path: str):
    strings = []
    for key1 in data_icon:
        strings.append('[' + key1 + ']')
        for key2 in data_icon[key1]:
            strings.append(key2 + '=' + data_icon[key1][key2])
    with open(path_ico, 'w') as ico:
        ico.write('\n'.join(strings))


if __name__ == '__main__':
    data_icon = parse_data_icon(path_ico)
    data_icon['InternetShortcut']['IconFile'] = path_exe
    data_icon_to_strings(data_icon, path_ico)
