import configparser
import yaml

# Токен бота
PARSER = configparser.ConfigParser()
PARSER.read("settings.ini")
BOT_TOKEN = PARSER['settings']['token'].strip().replace(' ', '')
BOOKS_PER_PAGE = int(PARSER['bot']['books_per_page'])
GENRES_PER_PAGE = int(PARSER['bot']['genres_per_page'])

PATH_DATABASE = "data/database.db"  # Путь к БД
PATH_LOGS = "data/logs.log"  # Путь к Логам

with open('data/strings.yml', 'r', encoding='utf-8') as f:
    STRINGS = yaml.load(f, yaml.Loader)


# Получение администраторов бота
def get_admins() -> list[int]:
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    admins = list(map(int, admins))

    return admins
