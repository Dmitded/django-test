import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

SUPERUSER_DATA = {
    'username': 'admin',
    'password': 'strongpass',
    'email': 'admin@mail.ru'
}

USER_DATA = {
    'username': 'test_user',
    'password': 'strongpass',
    'email': 'test_user@mail.ru'
}

USER_UPDATE_DATA = {
    'username': 'another_user',
    'email': 'another_user@mail.ru'
}

PASSPORT_DATA = {
    'first_name': 'Иван',
    'last_name': 'Иванов',
    'passport_series': 1234,
    'passport_number': 123456
}

PASSPORT_UPDATE_DATA = {
    'first_name': 'Семен',
    'last_name': 'Семенов',
    'passport_series': 4321,
    'passport_number': 654321
}
