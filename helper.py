import random
import string


class RandomUserData:
    """
    Класс для генерации случайных данных пользователя.
    """

    @staticmethod
    def random_string(length: int) -> str:
        """
        Генерирует случайную строку заданной длины,
        состоящую из строчных букв, цифр и специальных символов "_.-".

        :param length: длина генерируемой строки
        :return: случайная строка
        """
        special_symbols = "_.-"
        string_symbols = string.ascii_lowercase + string.digits + special_symbols
        return ''.join(random.choices(string_symbols, k=length))

    def user_data_generation(self) -> dict:
        """
        Генерирует словарь с данными пользователя:
        name, email и password.

        :return: словарь с ключами 'name', 'email', 'password'
        """
        user_data = {
            'name': self.random_string(12),
            'email': self.random_string(6) + '@gmail.com',
            'password': self.random_string(6)
        }
        return user_data