import secrets
import string


def generate_password(length=8):
    """
    Генерирует случайный пароль заданной длины.

    :param length: Длина пароля (по умолчанию 8).
    :return: Сгенерированный пароль.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(secrets.choice(alphabet) for i in range(length))

    return password

