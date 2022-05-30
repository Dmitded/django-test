from django.test import TestCase
from small_app.models import User, Passport
from .test_data import USER_DATA, USER_UPDATE_DATA, PASSPORT_DATA, PASSPORT_UPDATE_DATA


class UserTestCase(TestCase):
    def test_user_have_required_fields(self):

        user = User.objects.create_user(
            username=USER_DATA['username'],
            password=USER_DATA['password'],
            email=USER_DATA['email'],
        )
        user.save()

        self.assertEqual(user.username, USER_DATA['username'])
        self.assertEqual(user.email, USER_DATA['email'])
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.created_at)

    def test_user_update_fields(self):

        user = User.objects.create_user(
            username=USER_DATA['username'],
            password=USER_DATA['password'],
            email=USER_DATA['email'],
        )
        user.save()

        user = User.objects.update(**USER_UPDATE_DATA)
        user = User.objects.get(username=USER_UPDATE_DATA['username'])

        self.assertEqual(user.username, USER_UPDATE_DATA['username'])
        self.assertEqual(user.email, USER_UPDATE_DATA['email'])

    def test_user_delete(self):

        user = User.objects.create(**USER_DATA)
        user.save()

        response = User.objects.remove(user_id=user.id)

        self.assertEqual(response, True)


class PassportTestCase(TestCase):
    def test_passport_have_required_fields(self):

        passport = Passport.objects.create_passport(**PASSPORT_DATA)
        passport.save()

        self.assertEqual(passport.passport_series, PASSPORT_DATA['passport_series'])
        self.assertEqual(passport.passport_number, PASSPORT_DATA['passport_number'])
        self.assertEqual(passport.first_name, PASSPORT_DATA['first_name'])
        self.assertEqual(passport.last_name, PASSPORT_DATA['last_name'])

    def test_passport_update_fields(self):

        passport = Passport.objects.create_passport(**PASSPORT_DATA)
        passport.save()
        passport_id = passport.id

        passport = Passport.objects.update(**PASSPORT_UPDATE_DATA)
        passport = Passport.objects.get(id=passport_id)

        self.assertEqual(passport.passport_series, PASSPORT_UPDATE_DATA['passport_series'])
        self.assertEqual(passport.passport_number, PASSPORT_UPDATE_DATA['passport_number'])
        self.assertEqual(passport.first_name, PASSPORT_UPDATE_DATA['first_name'])
        self.assertEqual(passport.last_name, PASSPORT_UPDATE_DATA['last_name'])

    def test_passport_delete(self):

        passport = Passport.objects.create(**PASSPORT_DATA)
        passport.save()

        response = Passport.objects.remove(passport_id=passport.id)

        self.assertEqual(response, True)
