from utils import get_state, getStateForWrongMessages
from TelegramBot import TelegramBotOld
import config
# Проверка нажатия кнопки "Налаштування"
def choose_settings(message):
    return message.text == '\U00002699Налаштування'



tBot = TelegramBotOld(config.token)
# Проверка нажатия кнопки "Заказы"
def choose_orders(message):
    return message.text == '\U0001F4E6Мої замовлення'


# Проверка нажатия кнопки Имя в окне "Настройки"
def change_name(message):
    return get_state(message.chat.id) == 6 and message.text == 'Ім’я'

def MessageNotExcpectedAtSettings(message):
    return get_state(message.chat.id) == 6 and message.text != 'Ім’я' and message.text != 'Телефон' and message.text != '\U0001F3E0Початок'

# Проверка нажатия кнопки Телефон в окне настройки
def change_phone(message):
    return get_state(message.chat.id) == 6 and message.text == 'Телефон'


def change_language(message):
    return get_state(message.chat.id) == 6 and message.text == 'Мова'


# Проверка ввода телефона
def phone_entered(message):
    return get_state(message.chat.id) == 5


# Проверка ввода телефона в настройках
def settings_phone_entered(message):
    return get_state(message.chat.id) == 8


# Проверка ввода имени в настройках
def settings_name_entered(message):
    return get_state(message.chat.id) == 7


# Проверка ввода языка в насройках
def settings_language_changed(message):
    return get_state(message.chat.id) == 9


def pressed_faivorite(message):
    return get_state(message.chat.id) == 5 and message.text == 'Зберегти замовлення'

#Кнопка подтверждения номера
def pressedAcceptPhone(message):
    return message.text == 'Вірно'




#Кнопка повторного введения номера
def pressedDeclinedPhone(message):
    return message.text == 'Повторити введеня'


def checkSO(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'so'
    return call

def botRestart(message):
    return message.text == "Рестарт"

listOfButtons = ['\U0001F4C1Меню','\U0001F6CDКошик','\U0001F4E6Мої замовлення',"\U0001F4E2Новини","\U00002699Налаштування","\U00002753Допомога","\U0001F4C1","\U0001F6CD","\U0001F3E0",'Ще','Телефон','Ім’я','\U0001F3E0Початок','\U0001F3E0',"Зберегти замовлення"]

def WrongMessageAtHelp(message):
    try:
        return getStateForWrongMessages(message.chat.id) == "HELP" and message.text not in listOfButtons and message.text[0:2] != "ЩЕ"
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
        return None

def WrongMessageAtHome(message):
    try:
        return getStateForWrongMessages(message.chat.id) == "HOME" and message.text not in listOfButtons and message.text[0:2] != "ЩЕ"
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
            tBot.print_without_keyboard(394868826, "MISTAKE")
        return None

def WrongMessageAtMyOrders(message):
    try:

        return getStateForWrongMessages(message.chat.id) == "MyORDERS" and message.text not in listOfButtons and message.text[0:2] != "ЩЕ"
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
            tBot.print_without_keyboard(394868826, "MISTAKE")

        return None

def WrongMessageAtBasket(message):
    try:
        return getStateForWrongMessages(message.chat.id) == "BASKET" and message.text not in listOfButtons and message.text[0:2] != "ЩЕ"
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
            tBot.print_without_keyboard(394868826, "MISTAKE")
        return None

def WrongMessageAtNews(message):
    try:
        return getStateForWrongMessages(message.chat.id) == "NEWS" and message.text not in listOfButtons and message.text[0:2] != "ЩЕ"
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
            tBot.print_without_keyboard(394868826, "MISTAKE")
        return None

def WrongMessageAtMeals(message):
    try:
        return getStateForWrongMessages(message.chat.id) == "MEALS" and message.text not in listOfButtons and message.text[0:2] != "ЩЕ"
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
            tBot.print_without_keyboard(394868826, "MISTAKE")
        return None
def WrongMessageAtRestaurants(message):
    try:
        return getStateForWrongMessages(message.chat.id) == "REST" and message.text not in listOfButtons and message.text[0:2] != "ЩЕ"
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
            tBot.print_without_keyboard(394868826, "MISTAKE")
        return None
def WrongMessageAtSettings(message):
    try:
        return getStateForWrongMessages(message.chat.id) == "SETTINGS" and message.text[0:2] != 'ЩЕ' and message.text not in listOfButtons
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
            tBot.print_without_keyboard(394868826, "MISTAKE")
        return None
def WrongMessageAtPhonEntered(message):
    try:
        return getStateForWrongMessages(message.chat.id) == "PHONE_ENTERED" and message.text not in listOfButtons and message.text[0:2] != "ЩЕ"
    except TypeError:
        for i in range(10):
            tBot.print_without_keyboard(392635953, "MISTAKE")
            tBot.print_without_keyboard(394868826, "MISTAKE")
        return None