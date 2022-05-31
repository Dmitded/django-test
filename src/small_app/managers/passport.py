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
        filters: dict = {}
    ):
        passports = self.filter(**filters)
        amount = passports.count()

        return {
            'passports': passports.all(),
            'amount': amount
        }

    def remove(self, passport_id):

        passport = self.filter(id=passport_id).exists()

        if passport is False:
            return False

        self.filter(id=passport_id).delete()

        return True
