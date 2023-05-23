import telebot
from extensions import *
from config import *
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = """Здравствуйте, это расчет обмена валют!
Увидеть список доступных валют можно тут: /values
Вводите валюты и их количество без запятых, с пробелами
Информацию вводите в данном формате:
Валюта1 Валюта2 количество"""
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["help"])
def start(message: telebot.types.Message):
    text = """Вводите валюты и их количество без запятых, с пробелами
Увидеть список доступных валют можно тут: /values
Информацию вводите в данном формате: 
Валюта1 Валюта2 количество"""
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in currency:
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise ConvertException("Неверное количество параметров")
        answer = Convertor.get_price(*values)
    except ConvertException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message, answer)


bot.polling()