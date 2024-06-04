import telebot
import secret
import random
import datetime

# экземпляр бота
bot = telebot.TeleBot(secret.TOKEN)

# Список игроков
players = []

# Список доступных ролей
roles = ['Мирный житель', 'Мафия', 'Полицейский']

# начало игры
game_started = False

# Время начала дня и ночи
day_start_time = datetime.time(8, 0, 0)  # День начинается в 8:00
night_start_time = datetime.time(20, 0, 0)  # Ночь начинается в 20:00


# Функция для определения, идет ли сейчас день
def is_day_time():
    current_time = datetime.datetime.now().time()
    return day_start_time <= current_time < night_start_time


# Функция для определения, идет ли сейчас ночь
def is_night_time():
    current_time = datetime.datetime.now().time()
    return current_time >= night_start_time or current_time < day_start_time


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот для игры в мафию. Напиши /help для списка команд.")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message,
                 "Список доступных команд:\n/start - начать игру\n/help - список команд\n/rules - правила игры\n/join - присоединиться к игре\n/start_game - начать игру")


# Обработчик команды /rules
@bot.message_handler(commands=['rules'])
def handle_rules(message):
    rules_text = "Правила игры в Мафию:\n1. ..."
    bot.reply_to(message, rules_text)


# Обработчик команды /join
@bot.message_handler(commands=['join'])
def handle_join(message):
    global roles
    if not game_started:
        if len(roles) > 0:
            role = random.choice(roles)
            roles.remove(role)
            players.append({'user': message.from_user, 'role': role})
            bot.send_message(message.chat.id,
                             f"Вы присоединились к игре! Ваша роль была отправлена в личное сообщение.")
            bot.send_message(message.from_user.id, f"Ваша роль: {role}")
        else:
            bot.reply_to(message, "Все роли уже распределены.")
    else:
        bot.reply_to(message, "Игра уже началась, присоединение к игре невозможно.")


# Обработчик команды /start_game
@bot.message_handler(commands=['start_game'])
def handle_start_game(message):
    global game_started
    if len(players) >= 3:  # Проверяем, что есть как минимум 3 игрока для начала игры
        game_started = True
        bot.reply_to(message, "Игра началась! В городе " + str(len(players)) + " игроков.")
    else:
        bot.reply_to(message, "Недостаточно игроков для начала игры.")


# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global game_started
    if game_started:
        player = get_player_by_user(message.from_user)
        if player:
            if player['role'] == 'Мафия' and is_night_time():
                bot.reply_to(message, "Вы мафия и можете выбрать цель для убийства.")
            elif player['role'] == 'Полицейский' and is_night_time():
                bot.reply_to(message, "Вы полицейский и можете проверить роль одного игрока.")
            elif is_day_time():
                bot.reply_to(message, "День наступил. Вы можете проголосовать за подозреваемого.")
            else:
                bot.reply_to(message, "Сейчас не время для ваших действий.")
        else:
            bot.reply_to(message, "Вы не участвуете в игре.")
    else:
        bot.reply_to(message, "Игра еще не началась. Напишите /start_game, чтобы начать игру.")


# Функция для поиска игрока по его пользователю
def get_player_by_user(user):
    for player in players:
        if player['user'] == user:
            return player
    return None


# Запуск
bot.polling()
