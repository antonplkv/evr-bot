import shelve

import math
import datetime
from mysql.connector import connection
from config import shelve_name, shelve_date_name
import TelegramBot
import config
def keyboard_tuple(keyboard_list, count):
    """
    Функция генерирует tuple для клавиатуры из списка
    :param keyboard_list: список кнопок
    :param count: количество кнопок в строке
    :return: Список tuple.
    """
    tuple_list = []
    row = ()
    for i in range(0, len(keyboard_list)):
        if i > 0 and i % count == 0:
            tuple_list.append(row)
            row = (keyboard_list[i],)
        else:
            row += (keyboard_list[i],)
    if row != ():
        tuple_list.append(row)
    return tuple_list


def calc_full_price(basket):
    answer = 0
    for i in range(0, len(basket)):
        answer += basket[i][3] * basket[i][2]
    return answer

# Работа с shelve
# 0 - state
# 1 - meal_count
# 2 - basket
# 3 - meal last index
# 4 - full price
# 5 - name
# 6 - phone
# 7 - additional info
# 8 - resturant
# 9 - meals
# 10 - meals_count
# 11 - rest_zone
# 12 - rest
# 13 - корзина палочек (sticks_basket)
# 14 - позиция в корзине палочек (sticks_count)
# 15 - Имя пользователя
# 16 - Телефон пользователя
# 17 - Язык пользователя
# 18 - Сохраненные заказы



def set_meals(chat_id, meals):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[9] = meals
        storage[str(chat_id)] = plist


def set_name(chat_id, name):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[15] = name
        storage[str(chat_id)] = plist



def get_name(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][15]
            return answer
        except KeyError:
            return None



def set_order_date(chat_id,order_id):
    with shelve.open(shelve_date_name) as storage:
        now = datetime.datetime.now()
        storage[str(chat_id)+str(order_id)] = now.strftime("%d.%m.%Y")

def get_order_date(chat_id,order_id):
    with shelve.open(shelve_date_name) as storage:
        try:
            answer = storage[str(chat_id) + str(order_id)]
            return answer
        except KeyError:
            return None

def setStateNew(chat_id,state):
    with shelve.open(shelve_date_name) as storage:
        storage['0'+str(chat_id)] = state



def getStateNew(chat_id):
    with shelve.open(shelve_date_name) as storage:
        try:
            answer = storage['0' + str(chat_id)]
            return answer
        except KeyError:
            return None

#10 - STATE FOR WRONG MESSAGES
def setStateForWrongMessages(chat_id, state):
    with shelve.open(shelve_date_name) as storage:
        storage[str(chat_id) + '10'] = state

def getStateForWrongMessages(chat_id):
    with shelve.open(shelve_date_name) as storage:
        try:
            answer = storage[str(chat_id) +'10']
            return answer
        except KeyError:
            return "None"

def set_phone(chat_id, phone):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[16] = phone
        storage[str(chat_id)] = plist

def check_phone(phone):

    if phone == -1:
        return False
    elif phone[0] == '(' and phone[4] == ')':
        return True

    phone = list(phone)

    if phone[0] is '+' and len(phone) is 13:
        del phone[0:3]

        phone.insert(0,'(')
        phone.insert(4,')')
        phone.insert(5,' ')
        phone.insert(9,'-')
        phone.insert(12,'-')

        return ''.join(phone)

    elif phone[0] is '0' and len(phone) is 10:
        phone.insert(0, '(')
        phone.insert(4, ')')
        phone.insert(5, ' ')
        phone.insert(9, '-')
        phone.insert(12, '-')


        return ''.join(phone)

    elif phone[0] is '3' and len(phone) is 12:
        del phone[0:2]

        phone.insert(0,'(')
        phone.insert(3,')')
        phone.insert(4,' ')
        phone.insert(8,'-')
        phone.insert(11,'-')

        return ''.join(phone)
    else:
        return False


def reparseNumber(phone):
    if phone == -1:
        return True
    phone = list(phone)
    if phone[0] is '(' and phone[4] is ')':
        symbols = ['(',')',' ','-','-']
        for i in symbols:
            phone.remove(i)
        return ''.join(phone)
    elif phone[0] is '+':
        del phone[0:3]
        return ''.join(phone)

    elif phone[0] is '3' and len(phone) is 12:
        del phone[0:2]
        return ''.join(phone)

    else:
        return ''.join(phone)

def get_phone(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][16]
            return answer
        except KeyError:
            return None


def get_language(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][17]
            return answer
        except KeyError:
            return None


def set_language(chat_id, language):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[17] = language
        storage[str(chat_id)] = plist


def get_meals(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][9]
            return answer
        except KeyError:
            return None


def set_rest_zone(chat_id, rest_zone):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[11] = rest_zone
        storage[str(chat_id)] = plist


def get_rest_zone(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][11]
            return answer
        except KeyError:
            return None


def set_rest(chat_id, rest):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[12] = rest
        storage[str(chat_id)] = plist


def get_rest(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][12]
            return answer
        except KeyError:
            return None


def get_meals_count(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][10]
            return answer
        except KeyError:
            return None


def set_meals_count(chat_id, meals_count):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[10] = meals_count
        storage[str(chat_id)] = plist


def set_user(chat_id):
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = [-1, -1, [[-1]], -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, [[217, 2], [218, 0]],
                                 0, -1, -1, -1, [[-1]]]


def get_saved_orders(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][18]
            return answer
        except KeyError:
            return None





def set_saved_orders(chat_id, saved_orders):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[18] = saved_orders
        storage[str(chat_id)] = plist



def set_sticks_count(chat_id, sticks_count):
    """
    Устанавливает позицию в корзине для палочек
    :param chat_id: ссылка на пользователя
    :param sticks_count: количество, которое нужно установить
    :return: не возвращает значение
    """
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[14] = sticks_count
        storage[str(chat_id)] = plist


def get_sticks_count(chat_id):
    """
    Возврает порядковый номер позиции в корзине для палочек
    :param chat_id: ссылка на пользователя
    :return: порядковый номер в корзине для палочек
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][14]
            return answer
        except KeyError:
            return None


def get_sticks_basket(chat_id):
    """
    Возвращает корзину для палочек
    :param chat_id: Ссылка на пользователя
    :return: Корзина для палочек
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][13]
            return answer
        except KeyError:
            return None


def set_sticks_basket(chat_id, basket):
    """
    Установка полной корзины палочек
    :param chat_id: Ссылка на пользователя
    :param basket: корзина палочек
    :return: ничего не возвращает
    """
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[13] = basket
        storage[str(chat_id)] = plist


def set_state(chat_id, state):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[0] = state
        storage[str(chat_id)] = plist


def get_state(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][0]
            return answer
        except KeyError:
            return None


def get_meal_count(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][1]
            return answer
        except KeyError:
            return None


def set_meal_count(chat_id, meal_count):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[1] = meal_count
        storage[str(chat_id)] = plist


def get_basket(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][2]
            return answer
        except KeyError:
            return None


def set_full_basket(chat_id, basket_entry):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[2] = basket_entry
        storage[str(chat_id)] = plist


def set_basket(chat_id, basket_entry):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        if plist[2][0] == [-1]:
            plist[2][0] = basket_entry
        # добавление элемента перед соевым соусом
        elif int(plist[2][-1][0]) == 219:
            plist[2].insert(-1, basket_entry)
        else:
            plist[2].append(basket_entry)
        storage[str(chat_id)] = plist


def clear_basket(chat_id):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[2] = [[-1]]
        storage[str(chat_id)] = plist


def clear_sticks_basket(chat_id):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[13] = [[217, 2], [218, 0]]
        storage[str(chat_id)] = plist


def set_basket_entry_count(chat_id, entry_name, count):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        for i in range(0, len(plist[2])):
            if plist[2][i][0] == entry_name:
                plist[2][i][2] = count
                break
        storage[str(chat_id)] = plist


def set_meal_index(chat_id, meal_index):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[3] = meal_index
        storage[str(chat_id)] = plist


def get_meal_index(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][3]
            return answer
        except KeyError:
            return None


def get_full_price(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][4]
            return answer
        except KeyError:
            return None


def set_full_price(chat_id, full_price):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[4] = full_price
        storage[str(chat_id)] = plist


def set_custumer_name(chat_id, name):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[5] = name
        storage[str(chat_id)] = plist


def set_custumer_phone(chat_id, phone):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[6] = phone
        storage[str(chat_id)] = plist


def set_custumer_additional_info(chat_id, additional_info):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[7] = additional_info
        storage[str(chat_id)] = plist


def set_custumer_resturant(chat_id, resturant):
    with shelve.open(shelve_name) as storage:
        plist = storage[str(chat_id)]
        plist[8] = resturant
        storage[str(chat_id)] = plist


def choose_best_packing(pack_list, items_count):
    # pack_list( name, count, price)
    pack_item = []  # информация про упаковку конкретного товара
    # TODO убрать заглушку на отсутствие упаковки (или предусмотреть другую)
    if len(pack_list) == 0:  # Если упаковки нет, то делаем "пустую упаковку"
        pack_item.append(['Порожня тара', 2, 1, 0])  # name, quantity, pack_count, price
    else:
        for i in range(len(pack_list)):
            count = math.ceil(items_count/pack_list[i][1])
            pack_item.append([pack_list[i][0], pack_list[i][1], count, pack_list[i][2]])
    return pack_item


# Вычисление полной стоимости корзины
def count_full_price(bascket):
    if bascket == [[-1]]:
        return 0
    full_price = 0
    for i in range(len(bascket)):
        if TelegramBot.get_promotion(bascket[i][0]):
            full_price += (bascket[i][2] * bascket[i][3]) / 2  # Цена на количество
        else:
            full_price += (bascket[i][2] * bascket[i][3])
        for j in range(len(bascket[i][5])):
            full_price += bascket[i][5][j][2] * bascket[i][5][j][3]
    return full_price


def updateLog(telegramID, activity, order_info = ''):
    now = datetime.datetime.now()
    currentTime = now.strftime("%d.%m.%Y %H:%M")
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = "INSERT INTO user_log (telegram_id, activity, order_info, activity_time) VALUES ('{0}', '{1}', '{2}', '{3}');".format(str(telegramID),str(activity),str(order_info),str(currentTime))

    cursor = db_con.cursor()
    cursor.execute(query)

    db_con.commit()
    cursor.close()
    db_con.close()

def SetUserInfoDB(message):
    name = message.from_user.first_name()
    last = message.from_user.last_name()
    username = message.from_user.user_name()
    id = message.chat.id
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                        database=config.db_name)
    query = "INSERT INTO user_bot_info (first_name, last_name, username, user_number,user_id) VALUES ('{0}', '{1}', '{2}', '{3}',{4);".format(

    name,last,username,id)

    cursor = db_con.cursor()
    cursor.execute(query)
    db_con.commit()
    cursor.close()
    db_con.close()

def checkNumberInDb(phoneNumber):
    db_con = connection.MySQLConnection(user=config.db_user, password=config.db_password, host=config.db_host,
                                            database=config.db_name)
    query = "SELECT from user_info_bot user_id"
    cursor = db_con.cursor()
    cursor.execute(query)

    for (number,) in cursor:
        if phoneNumber == (number,):
            return False


    cursor.close()
    db_con.close()
    return True