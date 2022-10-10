import os
import string

full_path = '/home/misha/.config/yandex-browser/Default/Preferences'
dir_apps = "/home/misha/.config/yandex-browser/Default/Web Applications/Manifest Resources/"


def get_entry_desktop(app_id: str, icon_path: str, path_link: str) -> str:
    return string.Template('''#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Terminal=false
Type=Application
Name=
Exec=/opt/yandex/browser/yandex-browser --profile-directory=Default --app-id=$app_id
Icon=$icon_path
StartupWMClass=crx_$app_id
Actions=Delete;Edit;

[Desktop Action Delete]
Name=Delete
Name[ru]=Удалить ярлык
Exec=rm $path_link

[Desktop Action Edit]
Name=Edit
Name[ru]=Изменить ярлык
Exec=gedit $path_link
''').substitute(app_id=app_id, icon_path=icon_path, path_link=path_link)


if __name__ == '__main__':
    app_ids = os.listdir(dir_apps)
    for app_id in app_ids:
        icon_path = os.path.join(dir_apps, app_id, 'Icons', '256.png')
        path_link = "/home/misha/.local/share/applications/" + app_id + '.desktop'
        with open(path_link, "w") as file:
            file.write(get_entry_desktop(app_id, icon_path, path_link))
