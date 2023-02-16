import telebot
import traceback

from extensions import APIException, Convertor   # собственные модули из "extensions"
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])  #обработка команд пользвателя
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате:\n<название валюты> \
<в какую валюту перевести>\
<какую сумму>\nУвидеть список достуных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  #обработка списка валют
def values(message: telebot.types.Message):
    text = 'доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])  #обработка неверно введённых данных
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверные параметры!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
