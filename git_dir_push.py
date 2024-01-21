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
