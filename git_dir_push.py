import argparse
import os
import subprocess
# todo доделать
if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='dirs git push')
    # parser.add_argument("-lg", "--log_file", action='store', help='')
    # parser.add_argument("-m", "--move", action='store_true', help="delete source")
    # args = parser.parse_args()
    # paths = []
    command = 'git add --all . \n git commit -a -m "+" \n git push'
    with open('path_git.txt') as file:
        paths = list((map(lambda s: s.replace('\n', ''), file.readlines())))
        programs = []

        for path in paths:
            if os.path.exists(path):
                os.chdir(path)
            else:
                continue
            programs.append(subprocess.Popen(command, stdout=subprocess.PIPE))
        for program in programs:
            program.wait()
            print(program.communicate())

# set log_file="%~dp0"dirs_git_push_log.txt
# set error_file="%~dp0"dirs_git_push_error.txt
# echo > %log_file%
# echo > %error_file%
# for /f "usebackq tokens=*" %%a in ("%~dp0path_git.txt") do (
# IF EXIST "%%a" (
# echo "%%a" >> %log_file%
# echo "%%a" >> %error_file%
# cd /d "%%a"
# call :f
# ) else (
# echo not found "%%a" 2>> %error_file%
# )
# )
# exit
# :f
# git add --all . >> %log_file% 2>> %error_file%
# git commit -a -m '+'  >> %log_file% 2>> %error_file%
# git push >> %log_file% 2>> %error_file%

