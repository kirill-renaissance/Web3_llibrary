# This is a sample Python script.
import telebot
from telebot import types
from geopy.distance import geodesic as GD
from peewee import *


tst_location = [[54.676115, 25.264799]]


#Задача найти ближайший шкаф с белорусской книгой

bot = telebot.TeleBot("")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    key_location = types.ReplyKeyboardMarkup(resize_keyboard=True)


    add_host = types.KeyboardButton("Дадаць уладальніка")
    key_location.add(types.KeyboardButton("Шафа паблізу'", request_location=True), add_host)
    bot.send_message(message.from_user.id, "Гэты бот дапаможа знайсці найбліжэйшую лакацыю з беларускімі кнігамі.", reply_markup=key_location)





@bot.message_handler(content_types=['location'])
def echo_location(message):


    id = 0
    min_range = 9000
    for x in range(len(tst_location)):
            # записать id-самого ближайшего шкафа

        if min_range > GD([message.location.latitude, message.location.longitude], tst_location[x]).km:
            min_range = GD([message.location.latitude, message.location.longitude], tst_location[x]).km
            id = x
    bot.send_message(message.from_user.id, "Адрас з бліжэйшай шафы:")
    bot.send_venue(message.from_user.id, tst_location[id][0],tst_location[id][1], "IMAGURU", "Vytenio g. 18, Vilnius 03229")

def add_location(message):
    bot.send_message(message.from_user.id, "Ваша шафа дададзена")




@bot.message_handler(func=lambda message: True)

def echo_all(message):
    if message.text == "Дадаць уладальніка":
        bot.send_message(message.from_user.id, "Отправьте название хоста")
        bot.register_next_step_handler(message, add_name_host)
    else:
        send_welcome(message)

def add_name_host(message):

    bot.send_message(message.from_user.id, "Дашлі калі ласка месцазнаходжанне")
    bot.register_next_step_handler(message, add_location)

bot.infinity_polling()
