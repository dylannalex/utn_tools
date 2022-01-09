from utn_tools import bot
from getpass import getpass
from os import system

OPTIONS = {
    "email": 0,
    "autogestion": 1,
    "complete polls": 2,
}


def _get_account() -> tuple[str, str, str]:
    system("cls")
    username = input("$ Enter dni:\t\t")
    legajo = input("$ Enter legajo:\t\t")
    password = getpass("$ Enter password:\t")
    return username, legajo, password


def _show_options() -> None:
    system("cls")
    for k, v in OPTIONS.items():
        print(f"[{v}] {k}")


def menu() -> None:
    username, legajo, password = _get_account()
    utn_bot = None
    while True:
        _show_options()
        option = int(input("\n\n$ Enter option: "))
        if option == OPTIONS["complete polls"]:
            roll_bot = bot.RollBot(username, password, legajo)
            roll_bot.complete_rolls()

        if option == OPTIONS["email"]:
            if not utn_bot:
                utn_bot = bot.UtnBot(username, password, legajo)
            utn_bot.login("email")

        if option == OPTIONS["autogestion"]:
            if not utn_bot:
                utn_bot = bot.UtnBot(username, password, legajo)
            utn_bot.login("autogestion")
