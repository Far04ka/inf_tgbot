from telebot import types
import telebot
import os

token = "5795503325:AAFehhPLtER0_UfDKn68BiM0VE305D123TE"
bot = telebot.TeleBot(token)
mounth = ''


def yt_create(mounth):
    yt = open(f"{mounth}/yt.txt", 'r')
    yt_arr = [line.strip() for line in yt]
    yt.close()
    return yt_arr


def numbers(word):
    buff = ''
    try:
        for i in word:
            if i == '.':
                break
            elif i.isdigit():
                buff += i
        return int(buff)
    except:
        return 0


def create_markup(mounth):
    markup1 = types.ReplyKeyboardMarkup()
    files = os.listdir(fr"{mounth}")
    markup1.add(types.KeyboardButton('Назад'))
    markup1.add(types.KeyboardButton('Расписание'))
    buff = 1
    for i in range(16):
        for j in files:
            if j != ".DS_Store":
                if numbers(j) == buff:
                    markup1.add(types.KeyboardButton(f'{j}'))
                    buff += 1
    return markup1


# Создание начальной клавиатуры
arr = ["Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь"]
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
mar_files = os.listdir()
for i in arr:
    for j in mar_files:
        if j == i:
            markup.add(types.KeyboardButton(f"{j}"))


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Выбери месяц', reply_markup=markup)
    bot.register_next_step_handler(msg, next_step)


def next_step(message):
    global mounth
    mounth = message.text
    try:
        msg = bot.send_message(message.chat.id, "Выбери урок", reply_markup=create_markup(message.text))
        bot.register_next_step_handler(msg, mounth_les)
    except:
        msg = bot.send_message(message.chat.id, "Ты по-моему перепутал", reply_markup=markup)
        bot.register_next_step_handler(msg, next_step)


def mounth_les(message):
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выбери месяц', reply_markup=markup)
        bot.register_next_step_handler(msg, next_step)
    elif message.text == 'Расписание':
        bot.send_photo(message.chat.id, open(fr"{mounth}/Расписание.jpg", 'rb'))
        msg = bot.send_message(message.chat.id, "Расписание на месяц 👆")
        bot.register_next_step_handler(msg, mounth_les)
    else:
        mounth_arr = yt_create(mounth)
        try:
            buff = ''
            for i in message.text:
                if i != '.':
                    buff += i
                else:
                    break
            bot.send_message(message.chat.id, mounth_arr[int(buff) - 1])
            files = os.listdir(fr"{mounth}/{message.text}")
            for i in files:
                if i != ".DS_Store":
                    bot.send_document(message.chat.id, open(fr"{mounth}/{message.text}/{i}", "rb"))
            msg = bot.send_message(message.chat.id, '😎😎😎')
            bot.register_next_step_handler(msg, mounth_les)
        except:
            msg = bot.send_message(message.chat.id, "Что-то пошло не так")
            bot.register_next_step_handler(msg, mounth_les)


bot.infinity_polling()
