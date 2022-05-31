from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def get_by_passport_data(self, passport_series, passport_number, user_id=None):
        user = self.filter(
            passport_series=passport_series,
            passport_number=passport_number
        )

        if user_id is not None:
            user = user.exclude(id=user_id)

        return user.first()

    def get_by_filters(
        self,
        filters
    ):
        users = self.filter(**filters)
        amount = users.count()

        return {
            'users': users.all(),
            'amount': amount
        }

    def create_user(self, username, email, password):

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def remove(self, user_id):

        user = self.filter(id=user_id).exists()

        if user is False:
            return False

        self.filter(id=user_id).delete()

        return True
