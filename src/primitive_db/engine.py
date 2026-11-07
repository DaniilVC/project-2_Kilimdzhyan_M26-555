import prompt


def show_help() -> None:
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

def welcome() -> None:
    """
    Запускает приветственный экран и цикл обработки команд.
    """
    print("Первая попытка запустить проект!\n\n***")
    show_help()
    while True:
            try:
                _command = prompt.string("Введите команду: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nЗавершение работы программы.")
                break
            
            match _command:
                case "exit":
                    break
                case "help":
                    show_help()
                case _:
                    pass