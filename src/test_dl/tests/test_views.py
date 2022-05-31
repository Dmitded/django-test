import string
import random
import json

from django.test import TestCase
from small_app.models import User, Passport
from .test_data import (
    SUPERUSER_DATA, USER_DATA, PASSPORT_DATA,
    PASSPORT_UPDATE_DATA, BASE_URL
)


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class UserViewsTestCase(TestCase):
    def test_unauthorized_user(self):
        response = self.client.get(f'{BASE_URL}/api/users/current')
        self.assertEqual(response.status_code, 403)

    def test_authorized_user(self):
        user = User.objects.create_user(**USER_DATA)
        user.save()

        response = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['token'])
        self.assertEqual(response.data['username'], USER_DATA['username'])
        self.assertEqual(response.data['email'], USER_DATA['email'])

    def test_incorrect_token_auth(self):
        response = self.client.get(
            f'{BASE_URL}/api/users/current',
            HTTP_AUTHORIZATION=f'Bearer {get_random_string(12)}'
        )

        self.assertEqual(response.status_code, 403)

    def test_correct_login(self):
        user = User.objects.create_user(**USER_DATA)
        user.save()

        response = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['token'])
        self.assertEqual(response.data['username'], USER_DATA['username'])
        self.assertEqual(response.data['email'], USER_DATA['email'])

    def test_nonexistent_user_login(self):
        response = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        )

        self.assertEqual(response.status_code, 400)

    def test_incorrect_password_login(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        response = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': get_random_string(10)
            })
        )

        self.assertEqual(response.status_code, 400)

    def test_get_users(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        superuser = User.objects.create_superuser(**SUPERUSER_DATA)
        superuser.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': SUPERUSER_DATA['username'],
                'password': SUPERUSER_DATA['password']
            })
        ).data['token']

        response = self.client.get(
            f'{BASE_URL}/api/users_search',
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['users'], [])

    def test_get_user(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        superuser = User.objects.create_superuser(**SUPERUSER_DATA)
        superuser.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': SUPERUSER_DATA['username'],
                'password': SUPERUSER_DATA['password']
            })
        ).data['token']

        response = self.client.get(
            f'{BASE_URL}/api/users/{user.id}',
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)

    def test_get_passports(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        ).data['token']

        passport = Passport.objects.create(**PASSPORT_DATA)
        passport.save()

        response = self.client.get(
            f'{BASE_URL}/api/passports',
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['passports'], [])
        self.assertIsNotNone(response.data['amount'])

    def test_create(self):
        user = User.objects.create_user(**USER_DATA)
        user.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        ).data['token']

        response = self.client.post(
            f'{BASE_URL}/api/passports',
            content_type='application/json',
            data=PASSPORT_DATA,
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['passport_series'], PASSPORT_DATA['passport_series'])
        self.assertEqual(response.data['passport_number'], PASSPORT_DATA['passport_number'])
        self.assertEqual(response.data['first_name'], PASSPORT_DATA['first_name'])
        self.assertEqual(response.data['last_name'], PASSPORT_DATA['last_name'])

    def test_get_passport(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        ).data['token']

        passport = Passport.objects.create(**PASSPORT_DATA)
        passport.save()

        response = self.client.get(
            f'{BASE_URL}/api/passports/{passport.id}',
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 200)

    def test_update_passport(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        ).data['token']

        passport = Passport.objects.create(**PASSPORT_DATA)
        passport.save()

        response = self.client.patch(
            f'{BASE_URL}/api/passports/{passport.id}',
            content_type='application/json',
            data=PASSPORT_UPDATE_DATA,
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['passport_series'], PASSPORT_UPDATE_DATA['passport_series'])
        self.assertEqual(response.data['passport_number'], PASSPORT_UPDATE_DATA['passport_number'])
        self.assertEqual(response.data['first_name'], PASSPORT_UPDATE_DATA['first_name'])
        self.assertEqual(response.data['last_name'], PASSPORT_UPDATE_DATA['last_name'])

    def test_create_exist_passport_data(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        ).data['token']

        passport = Passport.objects.create(**PASSPORT_DATA)
        passport.save()

        response = self.client.post(
            f'{BASE_URL}/api/passports',
            content_type='application/json',
            data=PASSPORT_DATA,
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 400)

    def test_update_exist_passport_data(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        ).data['token']

        passport = Passport.objects.create(**PASSPORT_DATA)
        passport.save()

        another_passport = Passport.objects.create(**PASSPORT_UPDATE_DATA)
        another_passport.save()

        response = self.client.patch(
            f'{BASE_URL}/api/passports/{passport.id}',
            content_type='application/json',
            data=PASSPORT_UPDATE_DATA,
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_passport(self):

        user = User.objects.create_user(**USER_DATA)
        user.save()

        auth_token = self.client.post(
            f'{BASE_URL}/api/login',
            content_type='application/json',
            data=json.dumps({
                'username': USER_DATA['username'],
                'password': USER_DATA['password']
            })
        ).data['token']

        passport = Passport.objects.create(**PASSPORT_DATA)
        passport.save()

        response = self.client.delete(
            f'{BASE_URL}/api/passports/{passport.id}',
            HTTP_AUTHORIZATION=f'Bearer {auth_token}'
        )

        self.assertEqual(response.status_code, 200)
