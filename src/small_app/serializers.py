from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Passport


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        # Вызвать исключение, если не предоставлена почта.
        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in.',
                code=400
            )

        # Вызвать исключение, если не предоставлен пароль.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.',
                code=400
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.',
                code=404
            )

        elif not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.',
                code=403
            )

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'password', 'token'
        )
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """

        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class UserAdminSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UsersSerializer(serializers.ModelSerializer):

    users = UserAdminSerializer(many=True)
    amount = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('users', 'amount',)


class PassportCreateSerializer(serializers.ModelSerializer):
    """ Сериализация создания нового объекта Passport """

    passport_series = serializers.IntegerField(
        min_value=1000,
        max_value=9999,
        required=True
    )
    passport_number = serializers.IntegerField(
        min_value=100000,
        max_value=999999,
        required=True
    )

    class Meta:
        model = Passport
        fields = ('id', 'passport_series', 'passport_number', 'first_name', 'last_name',)

    def create(self, validated_data):
        if Passport.objects.get_by_passport_data(
            passport_series=validated_data['passport_series'],
            passport_number=validated_data['passport_number']
        ):
            raise serializers.ValidationError(
                detail='Passport with this passport data exists',
                code=403
            )

        return Passport.objects.create_passport(**validated_data)


class PassportSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов Passport. """

    passport_series = serializers.IntegerField(
        min_value=1000,
        max_value=9999,
        required=False
    )
    passport_number = serializers.IntegerField(
        min_value=100000,
        max_value=999999,
        required=False
    )

    class Meta:
        model = Passport
        fields = ('id', 'passport_series', 'passport_number', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        """ Выполняет обновление Passport. """

        passport_series = validated_data.pop('passport_series', None)
        passport_number = validated_data.pop('passport_number', None)

        if (
            passport_series and passport_number is None
            or passport_number and passport_series is None
        ):
            raise serializers.ValidationError(
                'Series and passport number must be transmitted at the same time'
            )
        elif passport_series and passport_number and Passport.objects.get_by_passport_data(
            passport_series=passport_series,
            passport_number=passport_number,
            passport_id=instance.id
        ) is not None:
            raise serializers.ValidationError(
                detail='Passport with this passport data exists',
                code=403
            )

        validated_data['passport_series'] = passport_series
        validated_data['passport_number'] = passport_number

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class PassportsSerializer(serializers.ModelSerializer):

    passports = PassportSerializer(many=True)
    amount = serializers.IntegerField()

    class Meta:
        model = Passport
        fields = ('passports', 'amount',)
