from EvrasiaBotAbstractInterface import EvrasiaBotAbstractInterface


class Bridge(EvrasiaBotAbstractInterface):
    def __init__(self):
        self.__implementation = None    # ссылка на класс-реализатор
