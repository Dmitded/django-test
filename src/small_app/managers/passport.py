from django.db import models


class PassportManager(models.Manager):

    def get_by_passport_data(self, passport_series, passport_number, passport_id=None):
        passport = self.filter(
            passport_series=passport_series,
            passport_number=passport_number,
        )

        if passport_id is not None:
            passport = passport.exclude(id=passport_id)

        return passport.first()

    def get_by_filters(
        self,
        passport_series=None,
        passport_number=None,
        first_name=None,
        last_name=None
    ):
        passports = self.filter()

        if passport_series:
            passports = passports.filter(passport_series=passport_series)

        if passport_number:
            passports = passports.filter(passport_number=passport_number)

        if first_name:
            passports = passports.filter(first_name__icontains=first_name)

        if last_name:
            passports = passports.filter(last_name__icontains=last_name)

        amount = passports.count()

        return {
            'passports': passports.all(),
            'amount': amount
        }

    def create_passport(
        self,
        first_name,
        last_name,
        passport_series=None,
        passport_number=None
    ):

        if passport_series is None:
            raise TypeError('Passport must have a passport_number.')

        if passport_number is None:
            raise TypeError('Passport must have a passport_number.')

        passport = self.model(
            first_name=first_name,
            last_name=last_name,
            passport_series=passport_series,
            passport_number=passport_number
        )
        passport.save()

        return passport

    def remove(self, passport_id):

        passport = self.filter(id=passport_id).exists()

        if passport is False:
            return False

        self.filter(id=passport_id).delete()

        return True
