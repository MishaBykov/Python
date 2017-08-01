import os


def for_file(file, result=[], search_words=[]):
    if file.is_file():
        with open(file.path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                for word in search_words:
                    if word in line:
                        result.append(line.replace("\n", ""))
    else:
        print("Пришла папка")
    return result


def f():
    result = []
    stack = [os.scandir(pathDir)]
    while stack:
        for i in stack.pop():
            if i.is_dir():
                stack.append(os.scandir(i.path))
            if i.is_file():
                result = for_file(i, result=result, search_words=words)
    return result

if __name__ == '__main__':
    pathDir = input("Введите путь:\n")
    words = input("Слова для поиска:\n").split()

    for i in f():
        print(i)
