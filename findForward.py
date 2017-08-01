import os


def for_file(result=[], file=os.DirEntry(), search_words=[]):
    if file.is_file():
        with open(file.path(), 'r') as f:
            lines = f.readlines()
            for line in lines:
                for word in search_words:
                    if word in line:
                        result.append(line)
    else:
        print("Пришла папка")
    return result


if __name__ == '__main__':
    pathDir = "C:\\Users\\Tom\\Desktop\\1"  # input("Введите путь:")
    stack = [os.scandir(pathDir)]
    while True:
        for i in stack.pop():
            i = os.DirEntry(i)
