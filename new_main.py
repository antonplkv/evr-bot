# Файл с новой реализацией бота через классы

# TODO Описать бот в терминах EvrasiaBot
# TODO удалить лишние включения

from TelegramBot import TelegramBotOld, get_busket_keyboard, get_mody_params, get_mody, TelegramBot
import config

from telebot import types
from utils import *
from TelegramBot import get_inline_keyboard, print_busket_item, show_busket, update_busket, choose_rest_keyboard, \
    rest_keyboard, get_start_keyboard

from mysql.connector import connection

from EvrasiaBot import EvrasiaBot

# TODO Конфигурация бота на запуск. Обернуть в функцию класса TelegramBot
implementation = TelegramBot(config.token)
EvrasiaBot = EvrasiaBot(implementation)


# Функция начала работы бота. Комбинирована с функцией основного экрана
@implementation.bot.message_handler(commands=['start'])
def start_message(message):
    EvrasiaBot.start_message(message)


if __name__ == '__main__':
    # Запуск бота "плохим методом"
    # TODO Обернуть в класс с ботом
    print('Запуск бота')
    EvrasiaBot.start_bad()
