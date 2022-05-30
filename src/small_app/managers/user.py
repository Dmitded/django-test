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
        passport_series=None,
        passport_number=None,
        first_name=None,
        last_name=None
    ):
        users = self.filter()

        if passport_series:
            users = users.filter(passport_series=passport_series)

        if passport_number:
            users = users.filter(passport_number=passport_number)

        if first_name:
            users = users.filter(first_name__icontains=first_name)

        if last_name:
            users = users.filter(last_name__icontains=last_name)

        amount = users.count()

        return {
            'users': users.all(),
            'amount': amount
        }

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError('Superuser must have a password.')

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
