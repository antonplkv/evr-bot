# TODO Описать интерфейс реализации бота телеграмм


class BotInterface:
    def print_message(self, message_id, message_text):
        raise NotImplemented()

    def start_polling(self):
        raise NotImplemented()

    def print_keyboard_message(self, message_id, message_text, message_keyboard):
        raise NotImplemented()

    def print_picture(self, message_id, photo_url):
        raise NotImplemented()

    def print_keyboard_picture(self, message_id, photo_url, message_keyboard):
        raise NotImplemented()

    def update_message_text(self, chat_id, message_id, message_text, message_keyboard):
        raise NotImplemented()

    def update_message_text_html(self, chat_id, message_id, message_text, message_keyboard):
        raise NotImplemented()

    def update_message_keyboard(self, chat_id, message_id, message_keyboard):
        raise NotImplemented()

    def print_keyboard_message_html(self, message_id, message_text, message_keyboard):
        raise NotImplemented()

    def get_keyboard(self, keyboard_rows):
        raise NotImplemented()
