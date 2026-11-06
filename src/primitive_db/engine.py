import prompt


def welcome():
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    prompt.string("Введите команду: ")
    return welcome()

if __name__ == '__main__':
    welcome()