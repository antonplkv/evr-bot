# Проверки нажатий клавиш в корзине с палочками


# Проверка нажатия кнопки оформления заказа в корзине (кнопка "Оформить")
def choosePayPressed(call):
    return call and call.data == 'checkout'


# Функция проверки нажатия на стрелку "Влево" в корзине палочек
def checkSticksLeft(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'sticks' and str_list[1] == 'left'
    return call


# Функция проверки нажатия на стрелку "Вправо" в корзине
def checkSticksRight(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'sticks' and str_list[1] == 'right'
    return call


# Функция проверки нажатия на стрелку "Вверх" в корзине
def checkSticksUp(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'sticks' and str_list[1] == 'up'
    return call


# Функция проверки нажатия на стрелку "Вниз" в корзине
def checkSticksDown(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'sticks' and str_list[1] == 'down'
    return call


# Функция проверки нажатия на кнопку "Крест" в корзине
def checkSticksCross(call):
    if call:
        str_list = call.data.split("_")
        return str_list[0] == 'sticks' and str_list[1] == 'cross'
    return call