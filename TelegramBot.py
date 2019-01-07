from BotInterface import BotInterface
import telebot
from telebot import types

from utils import *
import config
from mysql.connector import connection


# TODO Реализовать описанный интерфейс бота


class TelegramBot(BotInterface):
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def print_message(self, message_id, message_text):
        """
        Функция отправляет сообщение пользователю без клавиатуры
        :param message_id: Идентификатор пользователя
        :param message_text: Текст сообщения
        :return: Функция ничего не возвращает
        """
        self.bot.send_message(message_id, message_text, reply_markup=types.ReplyKeyboardRemove())

    def start_polling(self):
        """
        Функция начинает опрос бота методом polling
        :return:Функция ничего не возвращает
        """
        self.bot.polling(none_stop=True)

    def print_keyboard_message(self, message_id, message_text, message_keyboard):
        """
        Функция отправляет сообщение пользователю с клавиатурой
        :param message_id: Идентификатор пользователя
        :param message_text:  Текст сообщения
        :param message_keyboard: Клавиатура типа ReplyKeyboardMarkup
        :return: Функция ничего не возвращает
        """
        self.bot.send_message(message_id, message_text, reply_markup=message_keyboard)

    def print_picture(self, message_id, photo_url):
        self.bot.send_photo(message_id, photo_url)

    def print_keyboard_picture(self, message_id, photo_url, message_keyboard):
        self.bot.send_photo(message_id, photo_url, reply_markup=message_keyboard)

    def update_message_text(self, chat_id, message_id, message_text, message_keyboard):
        self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                   reply_markup=message_keyboard)

    def update_message_text_html(self, chat_id, message_id, message_text, message_keyboard):
        self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                   reply_markup=message_keyboard, parse_mode='HTML')

    def print_keyboard_message_html(self, message_id, message_text, message_keyboard):
        self.bot.send_message(message_id, message_text, reply_markup=message_keyboard, parse_mode='HTML')

    def get_keyboard(self, keyboard_rows):
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for i in range(len(keyboard_rows)):
            keyboard.row(*tuple(keyboard_rows[i]))
        return keyboard


# TODO Заменить старое содержание TelegramBot.py


class TelegramBotOld:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def print_message(self, message_id, message_text):
        """
        Функция отправляет сообщение пользователю
        :param message_id: Идентификатор пользователя
        :param message_text: Текст сообщения
        :return: Функция ничего не возвращает
        """
        # self.bot.send_message(message_id, message_text)
        self.bot.send_message(message_id, message_text, reply_markup=types.ReplyKeyboardRemove())

    def start_polling(self):
        """
        Функция начинает опрос бота методом polling
        :return:Функция ничего не возвращает
        """
        self.bot.polling(none_stop=True)

    def print_keyboard_message(self, message_id, message_text, message_keyboard):
        """
        Функция отправляет сообщение пользователю с клавиатурой
        :param message_id: Идентификатор пользователя
        :param message_text:  Текст сообщения
        :param message_keyboard: Клавиатура типа ReplyKeyboardMarkup
        :return: Функция ничего не возвращает
        """
        self.bot.send_message(message_id, message_text, reply_markup=message_keyboard)

    def print_without_keyboard(self, message_id, message_text):
        self.bot.send_message(message_id, message_text)

    def print_picture(self, message_id, photo_url):
        self.bot.send_photo(message_id, photo_url)

    def print_keyboard_picture(self, message_id, photo_url, message_keyboard):
        self.bot.send_photo(message_id, photo_url, reply_markup=message_keyboard)

    def update_message_text(self, chat_id, message_id, message_text, message_keyboard):
        self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                   reply_markup=message_keyboard)

    def update_message_text_html(self, chat_id, message_id, message_text, message_keyboard):
        self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                   reply_markup=message_keyboard, parse_mode='HTML')

    def update_message_keyboard(self, chat_id, message_id, message_keyboard):
        self.bot.edit_message_reply_markup(chat_id, message_id, reply_markup=message_keyboard)

    def print_keyboard_message_html(self, message_id, message_text, message_keyboard):
        self.bot.send_message(message_id, message_text, reply_markup=message_keyboard,parse_mode = 'HTML' )

    def sendPhoto(self, chat_id, photo, descr,keyboard):
        self.bot.send_photo(chat_id, photo, caption=descr,reply_markup=keyboard,parse_mode='HTML')

    # def print_message_hideKeyboard(self, message_id, message_text):
    #     """
    #     Функция отправляет сообщение пользователю, пряча клавиатуру
    #     :param message_id: Идентификатор пользователя
    #     :param message_text: Текст сообщения
    #     :return:
    #     """
    #     self.bot.send_message()


def get_keyboard(keyboard_tuple_list):
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in range(0, len(keyboard_tuple_list)):
        message_keyboard.row(*keyboard_tuple_list[i])
    return message_keyboard


def get_inline_keyboard(keyboard_tuple_list):
    message_keyboard = types.InlineKeyboardMarkup()
    for i in range(0, len(keyboard_tuple_list)):
        message_keyboard.row(*keyboard_tuple_list[i])
    return message_keyboard


def get_busket_keyboard(position_count, position_number, total_number, mody_row):
    inline_keyboard = types.InlineKeyboardMarkup()
    if mody_row:
        inline_keyboard.row(*mody_row[0])
    inline_keyboard.row(types.InlineKeyboardButton(text='\U0000274C', callback_data='basket_cross'),
                        types.InlineKeyboardButton(text='\U0001F53B', callback_data='basket_down'),
                        types.InlineKeyboardButton(text=str(position_count), callback_data='data'),
                        types.InlineKeyboardButton(text='\U0001F53A', callback_data='basket_up'))
    inline_keyboard.row(types.InlineKeyboardButton(text='\U000025C0', callback_data='basket_left'),
                        types.InlineKeyboardButton(text=str(position_number) + '/' + str(total_number),
                                                   callback_data='data'),
                        types.InlineKeyboardButton(text='\U000025B6', callback_data='basket_right'))
    inline_keyboard.row(
        types.InlineKeyboardButton(text='\U00002705 Оформити',
                                   callback_data='checkout'))
    return inline_keyboard


# TODO убрать basket_item_id из вызовов
def print_busket_item(bot_obj, chat_id, basket_item_id, position_count , position_number, total_number,
                      busket_item_name, busket_item_price, busket_item_picture, busket_item_mody,
                      busket_item_mody_pos):

    price_of_item = position_count * busket_item_price
    if get_promotion(basket_item_id):
        price_of_item = (position_count * busket_item_price) / 2
        message_text = ''
        message_text += 'Кошик:\n\n'
        message_text += '<a href="{0}">{1}</a>\n\n'.format(str(busket_item_picture), str(busket_item_name))
        message_text += '{0}грн. * {1} = {2} грн.'.format(str(busket_item_price), str(position_count),
                                                          str(price_of_item))
        message_text += '\nКількість акційних страв %d' % (int(position_count / 2))
        message_text += '\n\nЗагальна вартість замовлення з урахуванням упаковки становить {0} грн'.format(
            get_full_price(chat_id))
    else:
        message_text = ''
        message_text += 'Кошик:\n\n'
        message_text += '<a href="{0}">{1}</a>\n\n'.format(str(busket_item_picture), str(busket_item_name))
        message_text += '{0}грн. * {1} = {2} грн.'.format(str(busket_item_price), str(position_count),
                                                          str(price_of_item))
        message_text += '\n\nЗагальна вартість замовлення з урахуванням упаковки становить {0} грн'.format(
            get_full_price(chat_id))
    # Информация про модификаторы
    mody_params = get_mody_params(busket_item_mody, busket_item_mody_pos)
    mody_row = []
    if mody_params != [-1]:
        message_text += mody_params[0]
        mody_row = mody_params[1]

    if get_promotion(basket_item_id):
        position_count_key = int(position_count/2)
        inline_keyboard = get_busket_keyboard(position_count_key, position_number, total_number, mody_row)
        bot_obj.print_keyboard_message_html(chat_id, message_text, inline_keyboard)
    else:
        inline_keyboard = get_busket_keyboard(position_count, position_number, total_number, mody_row)
        bot_obj.print_keyboard_message_html(chat_id, message_text, inline_keyboard)


# TODO убрать basket_item_id из вызовов
def change_busket_item(bot_obj, chat_id, message_id, basket_item_id, position_count, position_number, total_number,
                       busket_item_name, busket_item_price, busket_item_picture, busket_item_mody,
                       busket_item_mody_pos):

    price_of_item = position_count * busket_item_price
    if get_promotion(basket_item_id):
        price_of_item = (position_count * busket_item_price) / 2
        message_text = ''
        message_text += 'Кошик:\n\n'
        message_text += '<a href="{0}">{1}</a>\n\n'.format(str(busket_item_picture), str(busket_item_name))
        message_text += '{0}грн. * {1} = {2} грн.'.format(str(busket_item_price), str(position_count),
                                                          str(price_of_item))
        message_text+= '\nКількість акційних страв %d'%(int(position_count/2))
        message_text += '\n\nЗагальна вартість замовлення з урахуванням упаковки становить {0} грн'.format(
            get_full_price(chat_id))
    else:
        message_text = ''
        message_text += 'Кошик:\n\n'
        message_text += '<a href="{0}">{1}</a>\n\n'.format(str(busket_item_picture), str(busket_item_name))
        message_text += '{0}грн. * {1} = {2} грн.'.format(str(busket_item_price), str(position_count),
                                                          str(price_of_item))
        message_text += '\n\nЗагальна вартість замовлення з урахуванням упаковки становить {0} грн'.format(
            get_full_price(chat_id))
    # Вывод информации про модификаторы
    mody_params = get_mody_params(busket_item_mody, busket_item_mody_pos)
    mody_row = []
    if mody_params != [-1]:
        message_text += mody_params[0]
        mody_row = mody_params[1]
    if get_promotion(basket_item_id):
        position_count_key = int(position_count / 2)
        inline_keyboard = get_busket_keyboard(position_count_key, position_number, total_number, mody_row)
        bot_obj.print_keyboard_message_html(chat_id, message_text, inline_keyboard)
    else:
        inline_keyboard = get_busket_keyboard(position_count, position_number, total_number, mody_row)
        bot_obj.print_keyboard_message_html(chat_id, message_text, inline_keyboard)



def show_busket(tBot, message, basket):
    if basket != [[-1]] and len(basket) > 0:

        total_number = len(basket)  # Количество продуктов в корзине
        basket = basket[get_meal_index(message.chat.id)]
        basket_item_id = basket[0]
        position_count = basket[3]# Количество единиц продукта

        position_number = int(get_meal_index(message.chat.id)) + 1  # Номер продукта в корзине
        busket_item_name = basket[1]  # Имя продукта
        busket_item_price = basket[2]  # Цена на продукт
        busket_item_picture = basket[4]  # Ссылка на изображение продукта
        busket_item_mody = basket[6]
        busket_item_mody_pos = basket[7]
        print_busket_item(tBot,
                          message.chat.id,
                          basket_item_id,
                          position_count,
                          position_number,
                          total_number,
                          busket_item_name,
                          busket_item_price,
                          busket_item_picture,
                          busket_item_mody,
                          busket_item_mody_pos)
    else:

        message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        message_keyboard.row('\U0001F3E0Початок')
        tBot.print_keyboard_message(message.chat.id, 'Кошик порожній.', message_keyboard)


def update_busket(tBot, message, message_id, basket):
    if basket != [[-1]] and len(basket) > 0:
        total_number = len(basket)
        basket = basket[get_meal_index(message.chat.id)]
        basket_item_id = basket[0]
        position_count = basket[3]
        position_number = int(get_meal_index(message.chat.id)) + 1
        busket_item_name = basket[1]
        busket_item_price = basket[2]
        busket_item_picture = basket[4]
        busket_item_mody = basket[6]
        busket_item_mody_pos = basket[7]
        change_busket_item(tBot,
                           message.chat.id,
                           message_id,
                           basket_item_id,
                           position_count,
                           position_number,
                           total_number,
                           busket_item_name,
                           busket_item_price,
                           busket_item_picture,
                           busket_item_mody,
                           busket_item_mody_pos)
    else:
        message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        message_keyboard.row('\U0001F3E0Початок')
        tBot.print_keyboard_message(message.chat.id, 'Кошик порожній.', message_keyboard)


def show_sticks_busket(tBot, message, basket):
    """
    Отображение корзины палочек
    :param tBot: Ссылка на бот
    :param message: Ссылка на сообщение
    :param basket: корзина для отображения
    :return: ничего не возвращает
    """
    if basket != [[-1]] and len(basket) > 0:
        total_number = len(basket)  # Количество продуктов в корзине
        basket = basket[get_sticks_count(message.chat.id)]
        position_count = basket[1]  # Количество единиц продукта
        position_number = int(get_sticks_count(message.chat.id)) + 1  # Номер продукта в корзине
        busket_item_name = ''  # Имя палочек
        busket_item_picture = ''  # Ссылка на изображение продукта
        # TODO Отвязать от жестких запросов к бд, передать отдельному классу (методу класса)
        # <editor-fold desc="Получение информации про имя палочек и изображение">
        language = 'ua'
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        query = 'SELECT d.name, g.image FROM descriptions AS d LEFT JOIN products AS p ON d.descriptiontable_id = ' \
                'p.id LEFT JOIN gallerys AS g ON p.id = g.gallerytable_id WHERE d.descriptiontable_type = ' \
                '"App\\\\Models\\\\Product" AND g.gallerytable_type = "App\\\\Models\\\\Product" AND ' \
                'd.descriptiontable_id = {0} AND d.lang = "{1}";'.format(str(basket[0]), language)
        cursor = db_con.cursor()
        cursor.execute(query)
        for (name, image) in cursor:
            busket_item_name = name
            busket_item_picture = 'http://evrasia.colors-run.com{0}'.format(image)
        cursor.close()
        db_con.close()
        # </editor-fold>
        print_sticks_item(tBot,
                          message.chat.id,
                          position_count,
                          position_number,
                          total_number,
                          busket_item_name,
                          busket_item_picture)
    else:
        message_keyboard = get_start_keyboard()
        tBot.print_keyboard_message(message.chat.id, 'Кошик порожній.', message_keyboard)


def get_busket_sticks_keyboard(position_count, position_number, total_number):
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.row(types.InlineKeyboardButton(text='\U0000274C', callback_data='sticks_cross'),
                        types.InlineKeyboardButton(text='\U0001F53B', callback_data='sticks_down'),
                        types.InlineKeyboardButton(text=str(position_count), callback_data='data'),
                        types.InlineKeyboardButton(text='\U0001F53A', callback_data='sticks_up'))
    inline_keyboard.row(types.InlineKeyboardButton(text='\U000025C0', callback_data='sticks_left'),
                        types.InlineKeyboardButton(text=str(position_number) + '/' + str(total_number),
                                                   callback_data='data'),
                        types.InlineKeyboardButton(text='\U000025B6', callback_data='sticks_right'))
    inline_keyboard.row(
        types.InlineKeyboardButton(text='\U00002705 Оформити',
                                   callback_data='sticks_checkout'))
    return inline_keyboard


def print_sticks_item(bot_obj, chat_id, position_count, position_number, total_number,
                      busket_item_name,  busket_item_picture):
    message_text = ''
    message_text += 'Кошик:\n\n'
    message_text += '<a href="{0}">{1}</a>\n\n'.format(str(busket_item_picture), str(busket_item_name))
    inline_keyboard = get_busket_sticks_keyboard(position_count, position_number, total_number)
    bot_obj.print_keyboard_message_html(chat_id, message_text, inline_keyboard)


def update_sticks_item(bot_obj, chat_id, message_id, position_count, position_number, total_number,
                       busket_item_name,  busket_item_picture):
    message_text = ''
    message_text += 'Кошик:\n\n'
    message_text += '<a href="{0}">{1}</a>\n\n'.format(str(busket_item_picture), str(busket_item_name))
    inline_keyboard = get_busket_sticks_keyboard(position_count, position_number, total_number)
    bot_obj.update_message_text_html(chat_id,
                                     message_id,
                                     message_text,
                                     inline_keyboard)


def update_sticks_busket(tBot, message, message_id, basket):
    if basket != [[-1]] and len(basket) > 0:
        total_number = len(basket)  # Количество продуктов в корзине
        basket = basket[get_sticks_count(message.chat.id)]
        position_count = basket[1]  # Количество единиц продукта
        position_number = int(get_sticks_count(message.chat.id)) + 1  # Номер продукта в корзине
        busket_item_name = ''  # Имя палочек
        busket_item_picture = ''  # Ссылка на изображение продукта
        # TODO Отвязать от жестких запросов к бд, передать отдельному классу (методу класса)
        # <editor-fold desc="Получение информации про имя палочек и изображение">
        language = 'ua'
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        query = 'SELECT d.name, g.image FROM descriptions AS d LEFT JOIN products AS p ON d.descriptiontable_id = ' \
                'p.id LEFT JOIN gallerys AS g ON p.id = g.gallerytable_id WHERE d.descriptiontable_type = ' \
                '"App\\\\Models\\\\Product" AND g.gallerytable_type = "App\\\\Models\\\\Product" AND ' \
                'd.descriptiontable_id = {0} AND d.lang = "{1}";'.format(str(basket[0]), language)
        cursor = db_con.cursor()
        cursor.execute(query)
        for (name, image) in cursor:
            busket_item_name = name
            busket_item_picture = 'http://evrasia.colors-run.com{0}'.format(image)
        cursor.close()
        db_con.close()
        # </editor-fold>
        update_sticks_item(tBot,
                           message.chat.id,
                           message_id,
                           position_count,
                           position_number,
                           total_number,
                           busket_item_name,
                           busket_item_picture)
    else:
        message_keyboard = get_start_keyboard()
        tBot.print_keyboard_message(message.chat.id, 'Кошик порожній.', message_keyboard)




def choose_rest_keyboard():
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    message_keyboard.row('Обрати ресторан')
    return message_keyboard


def rest_keyboard(rest_list):
    message_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    new_rest_list = []
    for i in range(0, len(rest_list)):
        new_rest_list.append(rest_list[i][1] + ' - 12:34')
    tuple_list = keyboard_tuple(new_rest_list, 2)
    for i in range(0, len(tuple_list)):
        message_keyboard.row(*tuple_list[i])
    return message_keyboard

def send_photo(self, chat_id, photo, descr):
    self.bot.send_photo(chat_id, photo, caption=descr)
def get_mody(product_id):
    product_modies = []
    # <editor-fold desc="Проверяем наличие модификаторов в базе и, если есть, запрашиваем информацию">
    # TODO вынести взаимодействие с базой в отдельную функцию
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    # Формируем запрос на получение информации про модификаторы
    query = 'SELECT p.mody_id FROM products AS p WHERE p.id = {0}'.format(str(product_id))
    cursor = db_con.cursor()
    cursor.execute(query)
    product_mody = []
    for (mody_id,) in cursor:
        product_mody.append(mody_id)
    cursor.close()
    db_con.close()
    if product_mody[0] == 0:  # если модификаторов нет
        return [-1]
    else:  # если модификаторы есть
        # Выполняем запрос на получение информации про модификаторы
        # <editor-fold desc="Запрос на получение модификаторов">
        db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
        # Формируем запрос на получение информации про модификаторы
        query = 'SELECT m.id, m.name FROM modies AS m WHERE m.parent = {0};'.format(str(product_mody[0]))
        cursor = db_con.cursor()
        cursor.execute(query)
        for (mody_id, mody_name) in cursor:
            product_modies.append([mody_id, mody_name])
        cursor.close()
        db_con.close()
        # </editor-fold>

    # </editor-fold>
    # Возвращаем в формате списка списков [mody_id, mody_name]
    return product_modies

def get_promotion(basket_entry_id):
    i = 0
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = 'SELECT id FROM products WHERE special = 1'
    cursor = db_con.cursor()
    cursor.execute(query)
    SpecialList = []
    for (id,) in cursor:
        special_item = [id]
        SpecialList.append(special_item)
    cursor.close()
    db_con.close()

    while i < len(SpecialList):
        if int(basket_entry_id) == int(SpecialList[i][0]):



            return True
            break
        else:
            pass

        i+=1
def get_mody_params(mody, mody_pos):
    product_modies = mody
    if product_modies == [-1]:
        return [-1]
    # <editor-fold desc="Формируем сообщение для вывода информации про модификаторы">
    mody_message = '\nДля цієї страви наявні наступні модифікатори:'
    for i in range(len(product_modies)):
        mody_message += '\n{0}. {1}'.format(str(i + 1), str(product_modies[i][1]))
    mody_message += '\nЗараз обрано модифікатор {0}'.format(str(product_modies[int(mody_pos)][1]))
    # </editor-fold>
    # <editor-fold desc="Формируем клавиатуру для модификаторов">
    keyboard_list = []
    for i in range(len(product_modies)):
        keyboard_list.append(types.InlineKeyboardButton(text=str(i + 1), callback_data='mody_{0}'.format(str(i))))
    mody_keyboard = keyboard_tuple(keyboard_list, len(product_modies))
    # </editor-fold>
    return [mody_message, mody_keyboard]


def get_in_menu_keyboard(number = 5):
    message_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if number != 0:

        message_keyboard.row('\U0001F3E0','\U0001F4C1','\U0001F6CD', 'ЩЕ '+ str(number) + ' ⏩')
    else:
        message_keyboard.row('\U0001F3E0', '\U0001F4C1', '\U0001F6CD')
    return message_keyboard

def get_start_keyboard():
    message_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    message_keyboard.row('\U0001F3E0Початок')
    return message_keyboard


def get_settings_keyboard():
    message_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    message_keyboard.row('Ім’я')
    message_keyboard.row('Телефон')
    message_keyboard.row('\U0001F3E0Початок')
    return message_keyboard


def get_start_back_keyboard():
    """
    Функция, которая возвращает клавиатуру с кнопками "Початок" и "Назад"
    :return: Функция возвращает клавиатуру.
    """
    message_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    message_keyboard.row('\U0001F3E0Початок', 'Назад')
    return message_keyboard


def get_change_start_back_keyboard(chat_id):
    """
    Функция, которая возвращает клавиатуру с кнопками "Початок" и "Назад"
    :return: Функция возвращает клавиатуру.
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Надіслати номер телефону", request_contact=True)
    button_okay = types.KeyboardButton(text="✅Вірно")
    button_back = types.KeyboardButton(text="Назад")
    button_decline = types.KeyboardButton(text="Скасувати")

    keyboard.add(button_okay,button_phone,button_back,button_decline)
    return keyboard

def get_name_keyboard(chat_id):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_okay = types.KeyboardButton(text="✅Вірно")
    button_back = types.KeyboardButton(text="Назад")
    button_decline = types.KeyboardButton(text="Скасувати")

    keyboard.add(button_okay, button_back, button_decline)
    return keyboard




def get_help_keyboard():
    message_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    message_keyboard.row('ПОСЛУГА', 'Дзвонити Оператору')
    return message_keyboard


def get_faivorite_keyboard():
    message_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    message_keyboard.row('\U0001F3E0Початок', 'Зберегти замовлення')
    return message_keyboard
