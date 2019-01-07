# pip install pytelegrambotapi
# pip install mysql-connector==2.1.6
from TelegramBot import TelegramBotOld, get_busket_keyboard, get_mody_params, get_mody, TelegramBot
import config

from telebot import types
from utils import *
from sticks_check import *
from checks import *
from TelegramBot import get_inline_keyboard, print_busket_item, show_busket, update_busket, choose_rest_keyboard, \
    rest_keyboard, get_start_keyboard, show_sticks_busket, update_sticks_busket, get_start_back_keyboard,\
    get_help_keyboard, get_settings_keyboard, get_change_start_back_keyboard, get_faivorite_keyboard

from mysql.connector import connection
import json
import base64
import requests

# START SERVER THINGS
import cherrypy
import config

WEBHOOK_HOST = '194.183.170.21'
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = 'https://%s:%s' % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/%s/' % config.token

# TODO Конфигурация бота на запуск. Обернуть в функцию класса TelegramBot
tBot = TelegramBotOld(config.token)
tBot.bot.remove_webhook()


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode('utf-8')
            update = types.Update.de_json(json_string)
            tBot.bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


# STOP SERVER THINGS

# START COPYING THINGS

# <editor-fold desc="Основная часть бота">
# Функция начала работы бота. Комбинирована с функцией основного экрана
@tBot.bot.message_handler(commands=['start'])
def start_message(message):
    # <editor-fold desc="Формирование клавиатуры">
    # TODO Отвязать от жестких строк. Предусмотреть мультиязычность
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    message_keyboard.row('\U0001F4C1Меню', '\U0001F6CDКошик')
    message_keyboard.row('\U0001F4E6Мої замовлення', '\U0001F4E2Новини')
    message_keyboard.row('\U00002699Налаштування', '\U00002753Допомога')
    # </editor-fold>
    # <editor-fold desc="Формирование имени-обращения к клиенту">
    # TODO Отвязать от жестких строк. Предусмотреть мультиязычность
    set_user(message.chat.id)
    if get_name(message.chat.id) != -1:
        greate_name = get_name(message.chat.id)
    else:
        greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
        if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
            greate_name += ' ' + message.from_user.last_name
    # </editor-fold>
    # Формирование окончательной строки-приветствия
    # TODO В будущем привязать к базе
    greate_message = 'Привет, %s! Я Мико - бот сети ресторанов Евразия. Помогу тебе в выборе блюд' % greate_name
    # Вывод на экран картинки-приветствия.
    # TODO Отвязать от жетской ссылки
    # tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/img/miko-3.2.jpg')
    tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/images/bot/M_ko_1024_500_2_text.png')
    # Вывод сообщения-приветствия
    tBot.print_keyboard_message(message.chat.id, greate_message, message_keyboard)
    # устанавливаем состояние пользователя
    set_state(message.chat.id, 1)


# Функция проверки нажатия на "Назад" из корзины палочек
def choose_back_to_basket(message):
    return message.text == 'Назад' and get_state(message.chat.id) == 3


def choose_back_to_sticks(message):
    return message.text == 'Назад' and get_state(message.chat.id) == 4


def choose_back_to_rest(message):
    return message.text == 'Назад' and get_state(message.chat.id) == 5


# Функция проверки нажатия кнопки "Новости"
def choose_news(message):
    return message.text == '\U0001F4E2Новини'


# Функция проверки нажатия кнопки "Помощь"
def choose_help(message):
    return message.text == '\U00002753Допомога'


# Функция проверки нажатия кнопки "ПОСЛУГА"
def choose_help_service(message):
    return message.text == 'ПОСЛУГА'


# Функция проверки нажатия кнопки "Дзвонити Оператору"
def choose_help_call(message):
    return message.text == 'Дзвонити Оператору'


# Проверка выбора зоны ресторана
def choose_rest_zone(call):
    if call:
        str_list = call.data.split("_")
        return 'restzone' == str_list[0]
    return call


# Проверка выбора ресторана
def choose_rest(call):
    if call:
        str_list = call.data.split("_")
        return 'rest' == str_list[0]
    return call


# Функция обработки выбора ресторана
@tBot.bot.callback_query_handler(func=choose_rest)
def rest_chosen(call):
    set_rest(call.message.chat.id, call.data.split('_')[1])
    message_keyboard = get_change_start_back_keyboard(call.message.chat.id)
    message_text = 'Будь-ласка, введіть номер телефону'
    tBot.print_keyboard_message(call.message.chat.id, message_text, message_keyboard)
    set_state(call.message.chat.id, 5)


# Функция отображения ресторанов конкретной зоны
@tBot.bot.callback_query_handler(func=choose_rest_zone)
def chooserest(call):
    str_split = call.data.split('_')
    rest_zone_id = str(str_split[1])  # Идентификатор зоны ресторанов
    if rest_zone_id == get_rest_zone(call.message.chat.id):
        return
    set_rest_zone(call.message.chat.id, rest_zone_id)  # Устанавливаем идентификатор зоны
    rest_list = []  # Список ресторанов в зоне
    # <editor-fold desc="Запросить информацию про рестораны в зоне">
    # TODO Вынести взаимодействие с БД в отдельный класс (список зон ресторанов).
    # TODO получать язык пользователя из настроек
    language = 'ua'
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT r.id, d.name FROM restaurants AS r LEFT JOIN descriptions_socials AS d ON r.id = ' \
            'd.descriptiontable_id WHERE d.descriptiontable_type = \"App\\\Models\\\Restaurants\" AND r.zone_id = {0}' \
            ' AND d.lang = \"{1}\";'.format(rest_zone_id, language)
    cursor = db_con.cursor()
    cursor.execute(query)
    for (id, name) in cursor:
        rest_list.append([id, name])
    cursor.close()
    db_con.close()
    # </editor-fold>
    # Формируем клавиатуру с ресторанами из зоны
    # <editor-fold desc="Формируем inline-клавиатуру с ресторанами">
    in_buttons = []  # список кнопок для ображения
    for i in range(0, len(rest_list)):
        in_buttons.append(
            types.InlineKeyboardButton(text=rest_list[i][1], callback_data='rest_{0}'.format(
                str(rest_list[i][0]))))
    # </editor-fold>
    # <editor-fold desc="Формируем клавиатуру с зонами ресторанов">
    restaurant_zone_list = []  # Список с информацией про зоны ресторанов
    # <editor-fold desc="Запрос информации про зоны ресторанов">
    # TODO Вынести взаимодействие с БД в отдельный класс (список зон ресторанов).
    # TODO получать язык пользователя из настроек
    language = 'ua'
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT c.id, d.name FROM categories as c LEFT JOIN descriptions_socials as d ON c.id = ' \
            'd.descriptiontable_id WHERE c.type = \"restaurants\" and d.descriptiontable_type = ' \
            '\"App\\\\Models\\\\Category\" and d.lang = \"{0}\";'.format(language)
    cursor = db_con.cursor()
    cursor.execute(query)
    for (id, name) in cursor:
        restaurant_zone_list.append([id, name])
    cursor.close()
    db_con.close()
    # </editor-fold>
    # Формируем клавиатуру с зонами ресторанов
    # <editor-fold desc="Формирование inline-клавиатуры с зонами ресторанов">
    for i in range(0, len(restaurant_zone_list)):
        in_buttons.append(
            types.InlineKeyboardButton(text=restaurant_zone_list[i][1], callback_data='restzone_{0}'.format(
                str(restaurant_zone_list[i][0]))))
    # </editor-fold>
    inline_keyboard = get_inline_keyboard(keyboard_tuple(in_buttons, 2))  # inline-клавиатура с ресторанами
    # </editor-fold>
    # TODO Реализовать мультиязычность (приглашение на выбор ресторана)
    message_text = 'Будь-ласка, оберіть ресторан'  # Текст для вывода информации
    tBot.update_message_text(call.message.chat.id, call.message.message_id, message_text, inline_keyboard)


# Проверка нажатия кнопки оформления заказа в корзине (кнопка "Оформити")
def chooseStickBascket(call):
    return call and call.data == 'checkout'


# Проверка нажания на клавишу выбора модификатора
def checkModyNumberPressed(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'mody'
    return call


# TODO Убрать опцию выбора оплаты заказа в ресторане или сразу
# Выбор оплаты сразу или в ресторане
def tempPressedPay(message):
    return message.text == 'Обрати ресторан'


# TODO убрать кнопку функции оплаты сразу
# Выбор функции сразу
def pressedPay(message):
    return message.text == 'Сплатити'


# TODO Изменить кнопку выбора оплаты в ресторане
# Выбор оплаты в ресторане
def pressedPayRest(message):
    return message.text == 'Сплатити в ресторані'


# TODO Убрать жесткую привязку к строке. Заменить на сравнение с переменной. Предусмотреть мультиязычность
# Кнопка перехода на основной экран бота
def pressedStart(message):
    return message.text == '\U0001F3E0Початок'


# TODO Убрать жесткую привязку к строке. Заменить на сравнение с переменной. Предусмотреть мультиязычность
# Кнопка перехода к меню
def pressedCatalog(message):
    return message.text == '\U0001F4C1Меню'


# TODO Убрать жесткую привязку к строке. Заменить на сравнение с переменной
# Функция проверки перехода к корзине
def pressedBasket(message):
    return message.text == '\U0001F6CDКошик'






# Экран выбора палочек
@tBot.bot.callback_query_handler(func=chooseStickBascket)
def choosesticks(call):
    set_state(call.message.chat.id, 3)
    set_sticks_count(call.message.chat.id, 0)
    basket = get_sticks_basket(call.message.chat.id)
    message_keyboard = get_start_back_keyboard()
    tBot.print_keyboard_message(call.message.chat.id, 'Кошик', message_keyboard)
    show_sticks_busket(tBot, call.message, basket)


# TODO изменить в связи с отменой функции оплаты?
# Экран выбора ресторана
@tBot.bot.callback_query_handler(func=choosePayPressed)
def chooserest(call):
    set_state(call.message.chat.id, 4)
    restaurant_zone_list = []  # Список с информацией про зоны ресторанов
    # <editor-fold desc="Запрос информации про зоны ресторанов">
    # TODO Вынести взаимодействие с БД в отдельный класс (список зон ресторанов).
    # TODO получать язык пользователя из настроек
    language = 'ua'
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT c.id, d.name FROM categories as c LEFT JOIN descriptions_socials as d ON c.id = ' \
            'd.descriptiontable_id WHERE c.type = \"restaurants\" and d.descriptiontable_type = ' \
            '\"App\\\\Models\\\\Category\" and d.lang = \"{0}\";'.format(language)
    cursor = db_con.cursor()
    cursor.execute(query)
    for (id, name) in cursor:
        restaurant_zone_list.append([id, name])
    cursor.close()
    db_con.close()
    # </editor-fold>
    # Формируем клавиатуру с зонами ресторанов
    # <editor-fold desc="Формирование inline-клавиатуры с зонами ресторанов">
    in_buttons = []  # список кнопок для ображения
    for i in range(0, len(restaurant_zone_list)):
        in_buttons.append(
            types.InlineKeyboardButton(text=restaurant_zone_list[i][1], callback_data='restzone_{0}'.format(
                str(restaurant_zone_list[i][0]))))
    inline_keyboard = get_inline_keyboard(keyboard_tuple(in_buttons, 2))  # inline-клавиатура с зонами ресторанов
    # </editor-fold>
    start_message_text = 'Вибір ресторану'
    start_message_keyboard = get_start_back_keyboard()
    tBot.print_keyboard_message(call.message.chat.id, start_message_text, start_message_keyboard)
    # TODO добавить мультиязычность
    message_text = 'Будь-ласка, оберіть регіон ресторану'  # Текст сообщения
    tBot.print_keyboard_message(call.message.chat.id, message_text, inline_keyboard)


# TODO изменить в связи с отменой функции оплаты?
# Экран выбора ресторанов
@tBot.bot.message_handler(func=tempPressedPay)
def tempPressedPay(message):
    # TODO Получение списка ресторанов
    # TODO Вынести получение списка ресторанов в иерархию взаимодействия с базой данных
    # <editor-fold desc="Получение списка ресторанов из базы данных">
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT descriptiontable_id, name FROM descriptions WHERE descriptiontable_type = ' \
            '"App\\\\Models\\\\Restaurants" and lang="ua" '
    cursor = db_con.cursor()
    cursor.execute(query)
    restaurant_list = []
    for (id, name) in cursor:
        cat_item = [id, name]
        restaurant_list.append(cat_item)
    cursor.close()
    db_con.close()
    # </editor-fold>
    # Вывод сообщения на экран
    tBot.print_keyboard_message(message.chat.id, 'Будь-ласка, оберіть ресторан:', rest_keyboard(restaurant_list))


# Функция перехода на основной экран
@tBot.bot.message_handler(func=pressedStart)
def user_message1(message):
    # TODO вынести формирование клавиатуры в отдельный метод
    # <editor-fold desc="Формирование основной клавиатуры">
    # TODO отвязать формирование клавиатуры от жестких строк. Предусмотреть возможность смены языка
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    message_keyboard.row('\U0001F4C1Меню', '\U0001F6CDКошик')
    message_keyboard.row('\U0001F4E6Мої Замовлення', '\U0001F4E2Новини')
    message_keyboard.row('\U00002699Налаштування', '\U00002753Допомога')
    # </editor-fold>
    # <editor-fold desc="Формирование приветствия по имени.">
    # TODO Отвязать от жесткой строки. Предусмотреть зависимость от языка
    if get_name(message.chat.id) != -1:
        greate_name = get_name(message.chat.id)
    else:
        greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
        if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
            greate_name += ' ' + message.from_user.last_name
    greate_message = 'Привет, %s! Я Мико - бот сети ресторанов Евразия. Помогу тебе в выборе блюд' % greate_name
    # </editor-fold>
    # Вывод на экран изображения
    # TODO отвязать от жесткой ссылки
    # tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/img/miko-3.2.jpg')
    tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/images/bot/M_ko_1024_500_2_text.png')
    # Вывод на экран привествия
    tBot.print_keyboard_message(message.chat.id, greate_message, message_keyboard)
    # Устанавливаем состояние пользователя в 1
    set_state(message.chat.id, 1)


# Функция перехода в корзину
@tBot.bot.message_handler(func=pressedBasket)
def user_pressed_basket(message):
    # TODO убрать привязку к жестким строкам. Предусмотреть мультиязычность
    set_meal_index(message.chat.id, 0)
    basket = get_basket(message.chat.id)
    message_keyboard = get_start_keyboard()
    tBot.print_keyboard_message(message.chat.id, 'Кошик', message_keyboard)
    show_busket(tBot, message, basket)
    set_state(message.chat.id, 2)  # установить состояние "В корзине"


# Функция вывода на экран меню.
@tBot.bot.message_handler(func=pressedCatalog)
def user_message(message):
    # <editor-fold desc="Формирование клавиатуры с переходом в начало">
    # TODO убрать привязку к жестким строкам. Предусмотреть мультиязычность.
    message_keyboard = get_start_keyboard()
    # </editor-fold>
    # Вывод на экран сообщения "Меню"
    # TODO отвязать от жесткой строки. Предусмотреть мультиязычсноть
    tBot.print_keyboard_message(message.chat.id, 'Меню', message_keyboard)
    # <editor-fold desc="Получение информации про категории меню из базы данных"
    # TODO Вынести взаимодействие с БД в отдельный класс (список категорий меню).
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT id FROM categories WHERE type = \'products\' and parent_id = 0 and is_online = 1'
    cursor = db_con.cursor()
    cursor.execute(query)
    cat_list = []
    for (id,) in cursor:
        cat_item = [id]
        cat_list.append(cat_item)
    cursor.close()
    db_con.close()
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    for i in range(0, len(cat_list)):
        query = 'SELECT name FROM descriptions WHERE descriptiontable_id = %s and lang = \'ua\' and ' \
                'descriptiontable_type = \'App\\\\Models\\\\Category\' '
        cursor = db_con.cursor()
        cursor.execute(query, (cat_list[i][0],))
        for (name,) in cursor:
            cat_list[i].append(name)
        cursor.close()
    db_con.close()
    # </editor-fold>
    # Если категории есть
    if len(cat_list) > 0:
        # <editor-fold desc="Формирование inline-клавиатуры с категориями меню">
        cat_names = []
        for i in range(0, len(cat_list)):
            cat_names.append([cat_list[i][1], cat_list[i][0]])
        in_buttons = []
        for i in range(0, len(cat_names)):
            in_buttons.append(
                types.InlineKeyboardButton(text=cat_names[i][0], callback_data='parent_' + str(cat_names[i][1])))
        inline_keyboard = get_inline_keyboard(keyboard_tuple(in_buttons, 2))
        # </editor-fold>
        # Вывод на экран списка категорий
        # TODO отвязать от жесткой строки. Предусмотреть мультиязычность
        tBot.print_keyboard_message(message.chat.id, 'Оберіть розділ', inline_keyboard)


# Функция проверки обращения к разделу меню
def checkCallbac(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'parent'
    return call


# Функция проверки обращения к отдельному товару ("Замовити")
def checkMeal(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'meal'
    return call


# Функция проверки нажатия на стрелку "Влево" в корзине
def checkBasketLeft(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'basket' and str_list[1] == 'left'
    return call


# Функция проверки нажатия на стрелку "Вправо" в корзине
def checkBasketRight(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'basket' and str_list[1] == 'right'
    return call


# Функция проверки нажатия на стрелку "Вверх" в корзине
def checkBasketUp(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'basket' and str_list[1] == 'up'
    return call


# Функция проверки нажатия на стрелку "Вниз" в корзине
def checkBasketDown(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'basket' and str_list[1] == 'down'
    return call


# Функция проверки нажатия на кнопку "Крест" в корзине
def checkBasketCross(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'basket' and str_list[1] == 'cross'
    return call


# Функция проверки нажатия на кнопку "Перейти в кошик"
def checkBasketPress(call):
    if call:
        return call.data == '\U0001F6CDКошик'
    return call


# Функция вывода корзины на экран
@tBot.bot.callback_query_handler(func=checkBasketPress)
def callback_basket_press(call):
    set_meal_index(call.message.chat.id, 0)
    basket = get_basket(call.message.chat.id)
    # <editor-fold desc="Формирование клавиатуры "Початок">
    # TODO отвязать от жесткой строки. Предусмотреть мультиязычсноть
    message_keyboard = get_start_keyboard()
    # </editor-fold>
    # Вывод сообщения "Кошик" на экран.
    # TODO отвязать от жесткой строки. Предусмотреть мультиязычность.
    tBot.print_keyboard_message(call.message.chat.id, 'Кошик', message_keyboard)
    # Вывод корзины на экран
    show_busket(tBot, call.message, basket)
    set_state(call.message.chat.id, 2)


# Функция обработки выбора модификации
@tBot.bot.callback_query_handler(func=checkModyNumberPressed)
def callback_mody_number_press(call):
    basket = get_basket(call.message.chat.id)
    if basket != [[-1]] and len(basket) > 0:
        if basket[get_meal_index(call.message.chat.id)][7] != int(call.data.split("_")[1]):
            basket[get_meal_index(call.message.chat.id)][7] = int(call.data.split("_")[1])
            set_full_basket(call.message.chat.id, basket)
            update_busket(tBot, call.message, call.message.message_id, basket)
        else:
            return


# Функция нажатия на крест в корзине
@tBot.bot.callback_query_handler(func=checkBasketCross)
def callback_basket_cross(call):
    basket = get_basket(call.message.chat.id)
    del basket[get_meal_index(call.message.chat.id)]
    if not basket:
        basket = [[-1]]
    set_full_basket(call.message.chat.id, basket)
    set_full_price(call.message.chat.id, count_full_price(basket))
    if get_meal_index(call.message.chat.id) != 0:
        set_meal_index(call.message.chat.id, get_meal_index(call.message.chat.id) - 1)
    update_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на стрелку вверх в корзине
@tBot.bot.callback_query_handler(func=checkBasketUp)
def callback_basket_up(call):
    basket = get_basket(call.message.chat.id)
    if basket != [[-1]] and len(basket) > 0:
        basket[get_meal_index(call.message.chat.id)][3] += 2
        # <editor-fold desc="Пересчет упаковки">
        pack_list = []
        for i in range(len(basket[get_meal_index(call.message.chat.id)][5])):
            pack_list.append([basket[get_meal_index(call.message.chat.id)][5][i][0],
                              basket[get_meal_index(call.message.chat.id)][5][i][1],
                              basket[get_meal_index(call.message.chat.id)][5][i][3]])
        bascket_item = choose_best_packing(pack_list,
                            basket[get_meal_index(call.message.chat.id)][3])
        basket[get_meal_index(call.message.chat.id)][5] = bascket_item
        # </editor-fold>
        clear_basket(call.message.chat.id)
        set_full_price(call.message.chat.id, count_full_price(basket))
        for i in range(0, len(basket)):
            set_basket(call.message.chat.id, basket[i])
        update_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на стрелку вниз в корзине
@tBot.bot.callback_query_handler(func=checkBasketDown)
def callback_basket_down(call):
    basket = get_basket(call.message.chat.id)
    if basket != [[-1]] and len(basket) > 0 and basket[get_meal_index(call.message.chat.id)][3] > 2:
        basket[get_meal_index(call.message.chat.id)][3] -= 2
        # <editor-fold desc="Пересчет упаковки">
        pack_list = []
        for i in range(len(basket[get_meal_index(call.message.chat.id)][5])):
            pack_list.append([basket[get_meal_index(call.message.chat.id)][5][i][0],
                              basket[get_meal_index(call.message.chat.id)][5][i][1],
                              basket[get_meal_index(call.message.chat.id)][5][i][3]])
        bascket_item = choose_best_packing(pack_list,
                                           basket[get_meal_index(call.message.chat.id)][3])
        basket[get_meal_index(call.message.chat.id)][5] = bascket_item
        # </editor-fold>
        clear_basket(call.message.chat.id)
        set_full_price(call.message.chat.id, count_full_price(basket))
        for i in range(0, len(basket)):
            set_basket(call.message.chat.id, basket[i])
        update_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на стрелку влево в корзине
@tBot.bot.callback_query_handler(func=checkBasketLeft)
def callback_basket_left(call):
    meal_index = get_meal_index(call.message.chat.id)
    if meal_index > 0:
        set_meal_index(call.message.chat.id, meal_index - 1)
        basket = get_basket(call.message.chat.id)
        update_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на стрелку вправо в корзине
@tBot.bot.callback_query_handler(func=checkBasketRight)
def callback_basket_right(call):
    meal_index = get_meal_index(call.message.chat.id)
    basket = get_basket(call.message.chat.id)
    if 0 <= meal_index < len(basket) - 1:
        set_meal_index(call.message.chat.id, meal_index + 1)
        basket = get_basket(call.message.chat.id)
        update_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на крест в корзине палочек
@tBot.bot.callback_query_handler(func=checkSticksCross)
def callback_sticks_cross(call):
    basket = get_sticks_basket(call.message.chat.id)
    del basket[get_sticks_count(call.message.chat.id)]
    if not basket:
        basket = [[-1]]
    set_sticks_basket(call.message.chat.id, basket)
    if get_sticks_count(call.message.chat.id) != 0:
        set_sticks_count(call.message.chat.id, get_sticks_count(call.message.chat.id) - 1)
    update_sticks_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на стрелку вверх в корзине палочек
@tBot.bot.callback_query_handler(func=checkSticksUp)
def callback_sticks_up(call):
    basket = get_sticks_basket(call.message.chat.id)
    if basket != [[-1]] and len(basket) > 0:
        basket[get_sticks_count(call.message.chat.id)][1] += 1
        set_sticks_basket(call.message.chat.id, basket)
        update_sticks_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на стрелку вниз в корзине палочек
@tBot.bot.callback_query_handler(func=checkSticksDown)
def callback_sticks_down(call):
    basket = get_sticks_basket(call.message.chat.id)
    if basket != [[-1]] and len(basket) > 0 and basket[get_sticks_count(call.message.chat.id)][1] > 0:
        basket[get_sticks_count(call.message.chat.id)][1] -= 1
        set_sticks_basket(call.message.chat.id, basket)
        update_sticks_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на стрелку влево в корзине палочек
@tBot.bot.callback_query_handler(func=checkSticksLeft)
def callback_sticks_left(call):
    sticks_count = get_sticks_count(call.message.chat.id)
    if sticks_count > 0:
        set_sticks_count(call.message.chat.id, sticks_count - 1)
        basket = get_sticks_basket(call.message.chat.id)
        update_sticks_busket(tBot, call.message, call.message.message_id, basket)


# Функция нажатия на стрелку вправо в корзине палочек
@tBot.bot.callback_query_handler(func=checkSticksRight)
def callback_sticks_right(call):
    sticks_count = get_sticks_count(call.message.chat.id)
    basket = get_sticks_basket(call.message.chat.id)
    if 0 <= sticks_count < len(basket) - 1:
        set_sticks_count(call.message.chat.id, sticks_count + 1)
        update_sticks_busket(tBot, call.message, call.message.message_id, basket)


# Функция добавления товара в корзину
@tBot.bot.callback_query_handler(func=checkMeal)
def callback_inline(call):
    # basket_entry
    # 0 - id
    # 1 - name
    # 2 - price
    # 3 - count
    # 4 - picture
    # 5 - pack
    # 6 - mody
    # 7 - mody_pos
    str_list = call.data.split('_')
    # <editor-fold desc="Получение информации о товаре через БД">
    # TODO вынести взаимодействие с БД в отдельный класс (Получение информации о товаре для корзины)
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT price FROM products WHERE id = %s'
    cursor = db_con.cursor()
    cursor.execute(query, (str_list[1],))
    cat_list = []
    for (price,) in cursor:
        cat_item = [price]
        cat_list.append(cat_item)
    cursor.close()
    db_con.close()
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT name FROM descriptions WHERE descriptiontable_type = \'App\\\\Models\\\\Product\' and ' \
            'descriptiontable_id = %s and lang = \'ua\' '
    for i in range(0, len(cat_list)):
        cursor = db_con.cursor()
        cursor.execute(query, (str_list[1],))
        for (name,) in cursor:
            cat_list[0].append(name)
        cursor.close()
    db_con.close()
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT image FROM gallerys WHERE gallerytable_type = \'App\\\\Models\\\\Product\' and gallerytable_id = ' \
            '%s '
    cursor = db_con.cursor()
    cursor.execute(query, (str_list[1],))
    check_flag = 0
    for (image,) in cursor:
        check_flag = 1
        # TODO базовую ссылку вынести из жесткой привязки к коду в config
        cat_list[0].append('http://evrasia.colors-run.com' + image)
    if check_flag != 1:
        cat_list[0].append(
            'http://evrasia.in.ua/sites/default/files/imagecache/w180/-%D0%B3%D1%80%D1%83%D0%BC%D0%B5-%D0%BC%D0%B0%D0'
            '%BA%D0%B8_0.jpg')
    cursor.close()
    db_con.close()
    pack_list = []  # список упаковок для единицы товара
    # <editor-fold desc="Получение информации про упаковку товара">
    # TODO предусмотреть мультиязычность
    language = 'ua'
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = ''
    if language == 'ua':
        query = 'SELECT p2.name, p1.quality, p2.price FROM packagings as p1 LEFT JOIN packing as p2 ON ' \
                'p1.packaging_id = p2.id WHERE p1.compact = 1 AND p1.product_id = ' + str_list[1] + '; '
    cursor = db_con.cursor()
    cursor.execute(query)
    for (name, count, price) in cursor:
        pack_list.append([name, count, price])
    cursor.close()
    db_con.close()
    # </editor-fold>
    # <editor-fold desc="Получение информации про модификаторы товара">
    mody = get_mody(str(str_list[1]))
    mody_pos = 0
    # </editor-fold>
    # </editor-fold>
    # TODO изменить количество товара в зависимости от акционности (или других условий)
    item_count = 2
    # <editor-fold desc="Вычисление количества упаковки">
    pack_item = choose_best_packing(pack_list, item_count)
    # </editor-fold>
    # Формирование окончательной информации о товаре
    basket_entry_id = str_list[1]
    basket_entry_name = cat_list[0][1]
    basket_entry_price = cat_list[0][0]
    basket_entry_picture = cat_list[0][2]
    basket_entry = [basket_entry_id, basket_entry_name, basket_entry_price, item_count, basket_entry_picture, pack_item,
                    mody, mody_pos]
    # Добавление информации о товаре в хранилище
    # TODO добавить соевый соус, если это первый товар в корзине
    # Если корзина пуста
    # <editor-fold desc="Добавление соевого соуса">
    if get_basket(call.message.chat.id) == [[-1]]:
        # Добавление соевого соуса жесткое
        soy_sause_id = 219  # жесткая привязка к id соевого соуса
        soy_sause_name = ''  # имя соевого соуса
        soy_sause_price = 0  # цена соевого соуса
        soy_sause_count = 2  # количество соевого соуса
        # TODO базовую ссылку вынести из жесткой привязки к коду в config
        soy_sause_picture = 'http://evrasia.colors-run.com'  # ссылка на изображение
        soy_sause_pack_item = [['Порожня тара', 2, 1, 0]]
        soy_sause_mody = [-1]  # информация про модификаторы
        soy_sause_mody_pos = -1  # информация про позицию модификаторов
        # <editor-fold desc="Запрос на получение информации по соусу (название, цена, картинка)">
        language = 'ua'
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        # TODO модифицировать запрос на получение информации по соевому соус
        query = 'SELECT d.name, p.price, g.image FROM descriptions AS d LEFT JOIN products as p ON ' \
                'd.descriptiontable_id = p.id LEFT JOIN gallerys as g ON p.id = g.gallerytable_id WHERE ' \
                'd.descriptiontable_type = "App\\\\Models\\\\Product" AND g.gallerytable_type = ' \
                '"App\\\\Models\\\\Product" AND d.descriptiontable_id = 219 AND d.lang = "ua"; '
        cursor = db_con.cursor()
        cursor.execute(query)
        for (name, price, picture) in cursor:
            soy_sause_name = name
            soy_sause_price = price
            soy_sause_picture += picture
        cursor.close()
        db_con.close()
        # </editor-fold>
        soy_sause_entry = [soy_sause_id,
                           soy_sause_name,
                           soy_sause_price,
                           soy_sause_count,
                           soy_sause_picture,
                           soy_sause_pack_item,
                           soy_sause_mody,
                           soy_sause_mody_pos]  # запись корзины с соевым соусом
        # Добавление соуса в корзину
        set_basket(call.message.chat.id, soy_sause_entry)
    # </editor-fold>
    set_basket(call.message.chat.id, basket_entry)
    # Установка новой полной цены
    set_full_price(call.message.chat.id, count_full_price(get_basket(call.message.chat.id)))
    # Изменение встроенной клавиатуры (дополнение кнопкой "Перейти в кошик")
    # Если клавиши "В кошик" еще нет, добавить ее
    if len(str_list) == 3:
        return
    # <editor-fold desc="Формирование новой клавиатуры">
    # TODO убрать привязку к жестким строкам. Предусмотреть мультиязычность
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.row(types.InlineKeyboardButton(text='Замовити', callback_data='meal_' + str(str_list[1]) + '_0'))
    inline_keyboard.row(types.InlineKeyboardButton('\U0001F6CDПерейти в Кошик',
                                                   callback_data='\U0001F6CDКошик'))
    # </editor-fold>
    # Обновление сообщения с новой клавиатурой
    tBot.update_message_keyboard(call.message.chat.id, call.message.message_id, inline_keyboard)


# Функция обращения к разделу меню.
@tBot.bot.callback_query_handler(func=checkCallbac)
def callback_inline(call):
    str_list = call.data.split('_')
    # <editor-fold desc="Получение информации по категориям из БД">
    # TODO вынести обращение к БД в отдельный класс (информация по категории)
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT id FROM categories WHERE type = \'products\' and parent_id = %s and is_online = 1'
    cursor = db_con.cursor()
    cursor.execute(query, (str_list[1],))
    cat_list = []
    for (id,) in cursor:
        cat_item = [id]
        cat_list.append(cat_item)
    cursor.close()
    db_con.close()
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    for i in range(0, len(cat_list)):
        query = 'SELECT name FROM descriptions WHERE descriptiontable_id = %s and lang = \'ua\' and ' \
                'descriptiontable_type = \'App\\\\Models\\\\Category\' '
        cursor = db_con.cursor()
        cursor.execute(query, (cat_list[i][0],))
        for (name,) in cursor:
            cat_list[i].append(name)
        cursor.close()
    db_con.close()
    # </editor-fold>
    # Если есть подкатегории
    # <editor-fold desc="Формирование списка категорий и вывод их на экран">
    if len(cat_list) > 0:
        cat_names = []
        for i in range(0, len(cat_list)):
            cat_names.append([cat_list[i][1], cat_list[i][0]])
        in_buttons = []
        for i in range(0, len(cat_names)):
            in_buttons.append(
                types.InlineKeyboardButton(text=cat_names[i][0], callback_data='parent_' + str(cat_names[i][1])))
        inline_keyboard = get_inline_keyboard(keyboard_tuple(in_buttons, 2))
        # Вывод на экран клавиатуры с категориями
        # TODO отвязать от жестких строк. Предусмотреть мультиязычность
        tBot.update_message_text(call.message.chat.id, call.message.message_id, 'Оберіть розділ', inline_keyboard)
    # </editor-fold>
    # Если нет подкатегорий и есть только товары
    else:
        # <editor-fold desc="Получение информации о товаре из БД">
        # TODO вынести взаимодействие с БД в отдельный класс (информация о товаре)
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        query = 'SELECT products.id, price, weight FROM products LEFT JOIN (category_product) ON (' \
                'category_product.product_id = products.id) WHERE category_product.category_id = %s and online = 1 '
        cursor = db_con.cursor()
        cursor.execute(query, (str_list[1],))
        cat_list = []
        for (id, price, weight) in cursor:
            cat_item = [id, price, weight]
            cat_list.append(cat_item)
        cursor.close()
        db_con.close()
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        query = 'SELECT name, description FROM descriptions_socials WHERE descriptiontable_type = ' \
                '\'App\\\\Models\\\\Product\' and descriptiontable_id = %s and lang = \'ua\' '
        for i in range(0, len(cat_list)):
            cursor = db_con.cursor()
            cursor.execute(query, (cat_list[i][0],))
            for (name, description) in cursor:
                cat_list[i].append(name)
                cat_list[i].append(description)
            cursor.close()
        db_con.close()
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        query = 'SELECT image FROM gallerys WHERE gallerytable_type = \'App\\\\Models\\\\Product\' and ' \
                'gallerytable_id = %s '
        for i in range(0, len(cat_list)):
            cursor = db_con.cursor()
            cursor.execute(query, (cat_list[i][0],))
            check_flag = 0
            for (image,) in cursor:
                check_flag = 1
                cat_list[i].append('http://evrasia.colors-run.com' + image)
            if check_flag != 1:
                cat_list[i].append(
                    'http://evrasia.in.ua/sites/default/files/imagecache/w180/-%D0%B3%D1%80%D1%83%D0%BC%D0%B5-%D0%BC'
                    '%D0%B0%D0%BA%D0%B8_0.jpg')
            cursor.close()
        db_con.close()
        # </editor-fold>
        # <editor-fold desc="Формирование клавиатуры со словом "Початок">
        # TODO отвязать от жесткой строки. Предусмотреть мультиязычнсоть.
        message_keyboard = get_start_keyboard()
        # </editor-fold>
        # Вывод сообщения "Меню"
        # TODO Отвязать от жесткой строки. Предусмотреть мультиязычность.
        tBot.print_keyboard_message(call.message.chat.id, 'Меню', message_keyboard)
        # Формирование списка товаров
        for i in range(0, len(cat_list)):
            # <editor-fold desc="Формирование встроенной клавиатуры "Заказать">
            # TODO Отвязать от жесткой строки. Предусмотреть мультиязычность.
            inline_keyboard = types.InlineKeyboardMarkup()
            inline_keyboard.add(
                types.InlineKeyboardButton(text='Замовити', callback_data='meal_' + str(cat_list[i][0])))
            # </editor-fold>
            # Вывод на экран изображения товара
            tBot.print_keyboard_picture(call.message.chat.id, cat_list[i][5], message_keyboard)
            # <editor-fold desc="Формирование сообщения с названием и описанием товара">
            # TODO Отвязать от жесткой строки. Предусмотреть мультиязычность
            message_str = '<b>{0}</b>\n\nВага: {1} г \n<b>Ціна: {2} грн</b>\n\n {3}'.format(cat_list[i][3],
                                                                                            str(cat_list[i][2]),
                                                                                            str(cat_list[i][1]),
                                                                                            cat_list[i][4])
            # </editor-fold>
            # Вывод сообщения с названием и описанием товара на экран
            tBot.print_keyboard_message_html(call.message.chat.id, message_str, inline_keyboard)


# Функция возврата к корзине
@tBot.bot.message_handler(func=choose_back_to_basket)
def back_to_basket(message):
    set_state(message.chat.id, 2)  # устанавливаем состояние корзины
    set_meal_index(message.chat.id, 0)
    basket = get_basket(message.chat.id)
    message_keyboard = get_start_keyboard()
    tBot.print_keyboard_message(message.chat.id, 'Кошик', message_keyboard)
    show_busket(tBot, message, basket)


# Функция возврата к палочкам
@tBot.bot.message_handler(func=choose_back_to_sticks)
def back_to_sticks(message):
    set_state(message.chat.id, 3)
    set_sticks_count(message.chat.id, 0)
    basket = get_sticks_basket(message.chat.id)
    message_keyboard = get_start_back_keyboard()
    tBot.print_keyboard_message(message.chat.id, 'Кошик', message_keyboard)
    show_sticks_busket(tBot, message, basket)


# Функция возврата к ресторанам
@tBot.bot.message_handler(func=choose_back_to_rest)
def back_to_rest(message):
    set_state(message.chat.id, 4)
    restaurant_zone_list = []  # Список с информацией про зоны ресторанов
    # <editor-fold desc="Запрос информации про зоны ресторанов">
    # TODO Вынести взаимодействие с БД в отдельный класс (список зон ресторанов).
    # TODO получать язык пользователя из настроек
    language = 'ua'
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT c.id, d.name FROM categories as c LEFT JOIN descriptions_socials as d ON c.id = ' \
            'd.descriptiontable_id WHERE c.type = \"restaurants\" and d.descriptiontable_type = ' \
            '\"App\\\\Models\\\\Category\" and d.lang = \"{0}\";'.format(language)
    cursor = db_con.cursor()
    cursor.execute(query)
    for (id, name) in cursor:
        restaurant_zone_list.append([id, name])
    cursor.close()
    db_con.close()
    # </editor-fold>
    # Формируем клавиатуру с зонами ресторанов
    # <editor-fold desc="Формирование inline-клавиатуры с зонами ресторанов">
    in_buttons = []  # список кнопок для ображения
    for i in range(0, len(restaurant_zone_list)):
        in_buttons.append(
            types.InlineKeyboardButton(text=restaurant_zone_list[i][1], callback_data='restzone_{0}'.format(
                str(restaurant_zone_list[i][0]))))
    inline_keyboard = get_inline_keyboard(keyboard_tuple(in_buttons, 2))  # inline-клавиатура с зонами ресторанов
    # </editor-fold>
    start_message_text = 'Вибір ресторану'
    start_message_keyboard = get_start_back_keyboard()
    tBot.print_keyboard_message(message.chat.id, start_message_text, start_message_keyboard)
    # TODO добавить мультиязычность
    message_text = 'Будь-ласка, оберіть регіон ресторану'  # Текст сообщения
    tBot.print_keyboard_message(message.chat.id, message_text, inline_keyboard)


# Функция отображения новостей
@tBot.bot.message_handler(func=choose_news)
def news(message):
    message_keyboard = get_start_keyboard()
    # TODO предусмотреть мультиязычность
    message_text = '<a href="{0}">{1}</a>'.format('https://t.me/EvrasiaUkraine', 'Офіційний канал Євразії')
    tBot.print_keyboard_message_html(message.chat.id, message_text, message_keyboard)


# Функция отображения основного меню помощи
@tBot.bot.message_handler(func=choose_help)
def helpb(message):
    # TODO Предусмотреть мультиязычность
    message_text = 'Допомога!'
    message_keyboard = get_help_keyboard()
    tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)


@tBot.bot.message_handler(func=choose_help_call)
def help_call(message):
    message_text = '+380445001717'
    message_keyboard = get_start_keyboard()
    tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)


# Описання функції Заберу сам
@tBot.bot.message_handler(func=choose_help_service)
def help_service(message):
    # TODO Предусмотреть мультиязычность
    message_text = '(где будет текст с описанием услуги Заберу Сам)'
    message_keyboard = get_start_keyboard()
    tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)


# Окно настроек
@tBot.bot.message_handler(func=choose_settings)
def settings_service(message):
    # Установка состояния "В разделе настроек"
    set_state(message.chat.id, 6)
    # TODO предусмотреть мультиязычность
    # <editor-fold desc="Формирование текста окна настроек">
    message_text = 'У Вас наступні налаштування:\n'
    message_text += 'Ім’я: '
    # Определение имени
    if get_name(message.chat.id) == -1:
        greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
        if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
            greate_name += ' ' + message.from_user.last_name
        set_name(message.chat.id, greate_name)
    message_text += get_name(message.chat.id) + '\n'

    message_text += 'Телефон: '
    # Определение телефона
    phone = get_phone(message.chat.id)
    if phone == -1:
        phone = '-'
    message_text += phone + '\n'

    # Определение языка
    message_text += 'Мова: '
    language = get_language(message.chat.id)
    if language == -1:
        language = '-'
    message_text += language + '\n'
    message_text += 'Оберіть, що бажаєте змінити, або натисніть клавішу "Початок"'
    # </editor-fold>
    # <editor-fold desc="Формирование клавиатуры настроек">
    message_keyboard = get_settings_keyboard()
    # </editor-fold>
    tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)


# Окно заказов
@tBot.bot.message_handler(func=choose_orders)
def orders_service(message):
    # TODO предусмотреть мультиязычность
    saved_orders = get_saved_orders(message.chat.id)
    first_message_text = 'Збережені замовлення'
    first_message_keyboard = get_start_keyboard()
    tBot.print_keyboard_message(message.chat.id, first_message_text, first_message_keyboard)
    if saved_orders != [[-1]]:
        message_text = 'Оберіть одне з Ваших збережених замовлень:'
        for i in range(len(saved_orders)):
            message_text += '\nЗбережене замовлення №{0}'.format(str(i+1))
        # <editor-fold desc="Формируем inline-клавиатуру с ресторанами">
        in_buttons = []  # список кнопок для ображения
        for i in range(0, len(saved_orders)):
            in_buttons.append(types.InlineKeyboardButton(text=str(i+1), callback_data='so_{0}'.format(str(i+1))))
        # </editor-fold>
        message_keyboard = get_inline_keyboard(keyboard_tuple(in_buttons, 5))
        tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)
    else:
        message_text = 'Збережених замовлень немає'
        message_keyboard = get_start_keyboard()
        tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)


# Окно установки имени
@tBot.bot.message_handler(func=change_name)
def name_change(message):
    message_keyboard = get_start_keyboard()
    message_text = 'Будь-ласка, введіть Ім’я'
    tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)
    set_state(message.chat.id, 7)


# Окно установки номера телефона
@tBot.bot.message_handler(func=change_phone)
def phone_change(message):
    message_keyboard = get_start_keyboard()
    message_text = 'Будь-ласка, введіть телефон'
    tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)
    set_state(message.chat.id, 8)





# Окно установки языка
@tBot.bot.message_handler(func=change_language)
def language_change(message):
    message_keyboard = get_start_keyboard()
    message_text = 'Будь-ласка, введіть мову'
    tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)
    set_state(message.chat.id, 9)


# Окно после установки имени
@tBot.bot.message_handler(func=settings_name_entered)
def settings_name(message):
    set_name(message.chat.id, message.text)
    # TODO вынести формирование клавиатуры в отдельный метод
    # <editor-fold desc="Формирование основной клавиатуры">
    # TODO отвязать формирование клавиатуры от жестких строк. Предусмотреть возможность смены языка
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    message_keyboard.row('\U0001F4C1Меню', '\U0001F6CDКошик')
    message_keyboard.row('\U0001F4E6Замовлення', '\U0001F4E2Новини')
    message_keyboard.row('\U00002699Налаштування', '\U00002753Допомога')
    # </editor-fold>
    # <editor-fold desc="Формирование приветствия по имени.">
    # TODO Отвязать от жесткой строки. Предусмотреть зависимость от языка
    if get_name(message.chat.id) != -1:
        greate_name = get_name(message.chat.id)
    else:
        greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
        if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
            greate_name += ' ' + message.from_user.last_name
    greate_message = 'Привет, %s! Я Мико - бот сети ресторанов Евразия. Помогу тебе в выборе блюд' % greate_name
    # </editor-fold>
    # Вывод на экран изображения
    # TODO отвязать от жесткой ссылки
    # tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/img/miko-3.2.jpg')
    tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/images/bot/M_ko_1024_500_2_text.png')
    # Вывод на экран привествия
    tBot.print_keyboard_message(message.chat.id, greate_message, message_keyboard)
    # Устанавливаем состояние пользователя в 1
    set_state(message.chat.id, 1)


# Окно после установки телефона
@tBot.bot.message_handler(func=settings_phone_entered)
def settings_phone(message):
    set_phone(message.chat.id, message.text)
    # TODO вынести формирование клавиатуры в отдельный метод
    # <editor-fold desc="Формирование основной клавиатуры">
    # TODO отвязать формирование клавиатуры от жестких строк. Предусмотреть возможность смены языка
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    message_keyboard.row('\U0001F4C1Меню', '\U0001F6CDКошик')
    message_keyboard.row('\U0001F4E6Замовлення', '\U0001F4E2Новини')
    message_keyboard.row('\U00002699Налаштування', '\U00002753Допомога')
    # </editor-fold>
    # <editor-fold desc="Формирование приветствия по имени.">
    # TODO Отвязать от жесткой строки. Предусмотреть зависимость от языка
    if get_name(message.chat.id) != -1:
        greate_name = get_name(message.chat.id)
    else:
        greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
        if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
            greate_name += ' ' + message.from_user.last_name
    greate_message = 'Привет, %s! Я Мико - бот сети ресторанов Евразия. Помогу тебе в выборе блюд' % greate_name
    # </editor-fold>
    # Вывод на экран изображения
    # TODO отвязать от жесткой ссылки
    # tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/img/miko-3.2.jpg')
    tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/images/bot/M_ko_1024_500_2_text.png')
    # Вывод на экран привествия
    tBot.print_keyboard_message(message.chat.id, greate_message, message_keyboard)
    # Устанавливаем состояние пользователя в 1
    set_state(message.chat.id, 1)


# Окно после установки языка
@tBot.bot.message_handler(func=settings_language_changed)
def settings_language(message):
    set_language(message.chat.id, message.text)
    # TODO вынести формирование клавиатуры в отдельный метод
    # <editor-fold desc="Формирование основной клавиатуры">
    # TODO отвязать формирование клавиатуры от жестких строк. Предусмотреть возможность смены языка
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    message_keyboard.row('\U0001F4C1Меню', '\U0001F6CDКошик')
    message_keyboard.row('\U0001F4E6Замовлення', '\U0001F4E2Новини')
    message_keyboard.row('\U00002699Налаштування', '\U00002753Допомога')
    # </editor-fold>
    # <editor-fold desc="Формирование приветствия по имени.">
    # TODO Отвязать от жесткой строки. Предусмотреть зависимость от языка
    if get_name(message.chat.id) != -1:
        greate_name = get_name(message.chat.id)
    else:
        greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
        if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
            greate_name += ' ' + message.from_user.last_name
    greate_message = 'Привет, %s! Я Мико - бот сети ресторанов Евразия. Помогу тебе в выборе блюд' % greate_name
    # </editor-fold>
    # Вывод на экран изображения
    # TODO отвязать от жесткой ссылки
    # tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/img/miko-3.2.jpg')
    tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/images/bot/M_ko_1024_500_2_text.png')
    # Вывод на экран привествия
    tBot.print_keyboard_message(message.chat.id, greate_message, message_keyboard)
    # Устанавливаем состояние пользователя в 1
    set_state(message.chat.id, 1)


@tBot.bot.message_handler(func=pressed_faivorite)
def pfaivorite(message):
    set_state(message.chat.id, 1)
    basket = get_basket(message.chat.id)
    sticks = get_sticks_basket(message.chat.id)
    clear_basket(message.chat.id)
    clear_sticks_basket(message.chat.id)
    new_saved = [basket, sticks]
    saved_orders = get_saved_orders(message.chat.id)
    if saved_orders == [[-1]]:
        saved_orders = [new_saved]
    elif len(saved_orders) < 5:
        saved_orders.append(new_saved)
    else:
        return
    set_saved_orders(message.chat.id, saved_orders)
    # <editor-fold desc="Формирование основной клавиатуры">
    # TODO отвязать формирование клавиатуры от жестких строк. Предусмотреть возможность смены языка
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    message_keyboard.row('\U0001F4C1Меню', '\U0001F6CDКошик')
    message_keyboard.row('\U0001F4E6Замовлення', '\U0001F4E2Новини')
    message_keyboard.row('\U00002699Налаштування', '\U00002753Допомога')
    # </editor-fold>
    # <editor-fold desc="Формирование приветствия по имени.">
    # TODO Отвязать от жесткой строки. Предусмотреть зависимость от языка
    if get_name(message.chat.id) != -1:
        greate_name = get_name(message.chat.id)
    else:
        greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
        if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
            greate_name += ' ' + message.from_user.last_name
    greate_message = 'Привет, %s! Я Мико - бот сети ресторанов Евразия. Помогу тебе в выборе блюд' % greate_name
    # </editor-fold>
    # Вывод на экран изображения
    # TODO отвязать от жесткой ссылки
    # tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/img/miko-3.2.jpg')
    tBot.print_picture(message.chat.id, 'http://evrasia.colors-run.com/images/bot/M_ko_1024_500_2_text.png')
    # Вывод на экран привествия
    tBot.print_keyboard_message(message.chat.id, greate_message, message_keyboard)
    # Устанавливаем состояние пользователя в 1
    set_state(message.chat.id, 1)


@tBot.bot.callback_query_handler(func=checkSO)
def callback_so_press(call):
    str_list = call.data.split("_")
    so_index = int(str_list[1])-1
    saved_orders = get_saved_orders(call.message.chat.id)
    basket = saved_orders[so_index][0]
    sticks = saved_orders[so_index][1]
    set_full_basket(call.message.chat.id, basket)
    set_sticks_basket(call.message.chat.id, sticks)
    set_meal_index(call.message.chat.id, 0)
    basket = get_basket(call.message.chat.id)
    # <editor-fold desc="Формирование клавиатуры "Початок">
    # TODO отвязать от жесткой строки. Предусмотреть мультиязычсноть
    message_keyboard = get_start_keyboard()
    # </editor-fold>
    # Вывод сообщения "Кошик" на экран.
    # TODO отвязать от жесткой строки. Предусмотреть мультиязычность.
    tBot.print_keyboard_message(call.message.chat.id, 'Кошик', message_keyboard)
    # Вывод корзины на экран
    show_busket(tBot, call.message, basket)
    set_state(call.message.chat.id, 2)


# Функция вывода на экран информации о заказе
@tBot.bot.message_handler(func=phone_entered)
def handle_message(message):
    if get_state(message.chat.id) == 5:
        rest_names = []
        # <editor-fold desc="Запрос имени ресторана">
        language = 'ua'
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        query = 'SELECT d.name FROM descriptions_socials AS d WHERE d.descriptiontable_type = ' \
                '\"App\\\\Models\\\\Restaurants\" AND d.descriptiontable_id = {0} AND d.lang = \"{1}\";'.format(
            str(get_rest(message.chat.id)), language)
        cursor = db_con.cursor()
        cursor.execute(query)
        for (name,) in cursor:
            rest_names.append(name)
        cursor.close()
        db_con.close()
        # </editor-fold>
        message_text = 'Замовлення прийняте!'
        message_text += '\n\nВаше замовлення на суму {0}грн. з урахуванням упаковки оформлене і відправлено до ' \
                        'ресторану на {1}. Очікуйте на дзвінок оператора.'.format(str(get_full_price(message.chat.id)),
                                                                                  str(rest_names[0]))
        # <editor-fold desc="Отправка информации про заказ">
        if get_name(message.chat.id) != -1:
            greate_name = get_name(message.chat.id)
        else:
            greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
            if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
                greate_name += ' ' + message.from_user.last_name
        user_name = greate_name  # имя пользователя
        user_phone = message.text  # номер телефона пользователя
        user = {'name': user_name, 'phone': user_phone}
        # TODO убрать обращение к бд при формировании json в заказе
        # <editor-fold desc="Получение информации про ресторан">
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        query = 'SELECT online_code FROM restaurants WHERE id = {0};'.format(str(get_rest(message.chat.id)))
        cursor = db_con.cursor()
        cursor.execute(query)
        for (rest_id,) in cursor:
            restaurant_id = rest_id  # идентификатор ресторана
        cursor.close()
        db_con.close()
        # </editor-fold>
        # restaurant_id = int(get_rest(message.chat.id))  # идентификатор ресторана
        order_id = 0  # идентификатор заказа
        order_type = 'bot'  # пометка бота
        basket = get_basket(message.chat.id)
        order_products = []  # информация по продуктам
        for i in range(len(basket)):
            # <editor-fold desc="Получение кода продукта из базы">
            order_code = 0
            db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                                database=config.db_name)
            query = 'SELECT global_code FROM products WHERE id = {0};'.format(str(basket[i][0]))
            cursor = db_con.cursor()
            cursor.execute(query)
            for (global_code,) in cursor:
                order_code = global_code  # код продукта
            cursor.close()
            db_con.close()
            # </editor-fold>
            # order_code = int(basket[i][0])  # код продукта
            order_quantity = int(basket[i][3])  # количество продукта
            order_mody = int(basket[i][6][basket[i][7]][0]) if basket[i][6] != [-1] else 0
            order_type_pack = 0
            order_products.append({'code': order_code, 'quantity': order_quantity, 'mody': order_mody, 'type_pack': order_type_pack})
        basket = get_sticks_basket(message.chat.id)
        for i in range(len(basket)):
            order_quantity = int(basket[i][1])
            if order_quantity == 0:
                continue
            # <editor-fold desc="Получение кода продукта из базы">
            order_code = 0
            db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                                database=config.db_name)
            query = 'SELECT global_code FROM products WHERE id = {0};'.format(str(basket[i][0]))
            cursor = db_con.cursor()
            cursor.execute(query)
            for (global_code,) in cursor:
                order_code = global_code  # код продукта
            cursor.close()
            db_con.close()
            # </editor-fold>
            # order_code = basket[i][0]
            order_mody = 0
            order_type_pack = 0
            order_products.append(
                {'code': order_code, 'quantity': order_quantity, 'mody': order_mody, 'type_pack': order_type_pack})
        order_total = '{0:.2f}'.format(get_full_price(message.chat.id))  # информация про общую сумму заказа
        order = {'id': order_id, 'type': order_type, 'products': order_products, 'total': order_total}
        # order = {'id': order_id, 'products': order_products, 'total': order_total}
        # order = {'products': order_products, 'total': order_total}
        # time = {'minute': 0, 'hour': 0}
        # data = {'user': user, 'restaurant_id': restaurant_id, 'order': order, 'time': time}
        data = {'user': user, 'restaurant_id': restaurant_id, 'order': order}
        json_data = json.dumps(data, separators=(',', ': '))
        print(json_data)
        encode_data = base64.b64encode(json_data.encode())
        r = requests.post('http://194.183.170.22/telegram/import', data={'code': encode_data})
        print(r)
        # </editor-fold>
        saved_orders = get_saved_orders(message.chat.id)
        if saved_orders == [[-1]] or len(saved_orders) < 5:
            message_keyboard = get_faivorite_keyboard()
        else:
            clear_basket(message.chat.id)
            clear_sticks_basket(message.chat.id)
            message_keyboard = get_start_keyboard()
            set_state(message.chat.id, 1)
        tBot.print_keyboard_message(message.chat.id, message_text, message_keyboard)
        set_rest_zone(message.chat.id, -1)
        # clear_basket(message.chat.id)


# </editor-fold>

# END COPYING THINGS


tBot.bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
