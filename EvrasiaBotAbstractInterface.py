"""
Интерфейс для создания бота. Необходимо реализовать
"""

# TODO Разработать интерфейс конечного бота


class EvrasiaBotAbstractInterface:
    def start_message(self, message):
        raise NotImplemented()

    def start_bad(self):
        raise NotImplemented()
