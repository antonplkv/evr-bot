from Bridge import Bridge
# TODO почистить import в EvraasiaBot
from utils import *

# TODO Реализовать разработанный интерфейс


class EvrasiaBot(Bridge):
    def __init__(self, implementation):
        self.__implementation = implementation

    def start_message(self, message):
        # <editor-fold desc="Формирование клавиатуры">
        # TODO Отвязать от жестких строк. Предусмотреть мультиязычность
        keyboard_rows = [
            ['\U0001F4C1Меню', '\U0001F6CDКошик'],
            ['\U0001F4E6Мої замовлення', '\U0001F4E2Новини'],
            ['\U00002699Налаштування', '\U00002753Допомога']
        ]
        message_keyboard = self.__implementation.get_keyboard(keyboard_rows)
        # </editor-fold>
        # <editor-fold desc="Формирование имени-обращения к клиенту">
        # TODO Отвязать от жестких строк. Предусмотреть мультиязычность
        greate_name = message.from_user.first_name if message.from_user.first_name is not None else 'любимый клиент'
        if greate_name != 'любимый клиент' and message.from_user.last_name is not None:
            greate_name += ' ' + message.from_user.last_name
        # </editor-fold>
        # Формирование окончательной строки-приветствия
        # TODO В будущем привязать к базе
        greate_message = 'Привет, %s! Я Мико - бот сети ресторанов Евразия. Помогу тебе в выборе блюд' % greate_name
        # Вывод на экран картинки-приветствия.
        # TODO Отвязать от жетской ссылки
        self.__implementation.print_picture(message.chat.id, 'http://evrasia.colors-run.com/img/miko-3.2.jpg')
        # Вывод сообщения-приветствия
        self.__implementation.print_keyboard_message(message.chat.id, greate_message, message_keyboard)
        # устанавливаем состояние пользователя
        set_user(message.chat.id)
        set_state(message.chat.id, 1)

    def start_bad(self):
        self.__implementation.start_polling()

