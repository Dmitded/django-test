from rest_framework import status, exceptions
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from .models import User, Passport
from .serializers import (
    RegistrationSerializer, LoginSerializer, UserSerializer,
    UsersSerializer, UserAdminSerializer, PassportCreateSerializer,
    PassportSerializer, PassportsSerializer
)
from .renders import UserJSONRenderer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthenticationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsersSerializer

    def retrieve(self, request, *args, **kwargs):

        users = User.objects.get_by_filters(**request.query_params.dict())
        serializer = self.serializer_class(users)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAdminAPIView(APIView):

    permission_classes = (IsAuthenticated, IsAdminUser)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserAdminSerializer

    def get(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            raise exceptions.APIException(detail=e, code=404)

        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            raise exceptions.APIException(detail=e, code=404)

        user.delete()

        return Response({}, status=status.HTTP_200_OK)


class PassportsApiView(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    # serializer_class = PassportsSerializer

    def get(self, request, *args, **kwargs):

        filters = {
            key: value for key, value in request.query_params.dict().items()
            if key in ('first_name', 'last_name', 'passport_series', 'passport_number')
        }

        passports = Passport.objects.get_by_filters(**filters)
        serializer = PassportsSerializer(passports)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        passport_data = request.data

        serializer = PassportCreateSerializer(data=passport_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PassportAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PassportSerializer

    def get(self, request, passport_id):
        try:
            passport = Passport.objects.get(id=passport_id)
        except Passport.DoesNotExist as e:
            raise exceptions.APIException(detail=e, code=404)

        serializer = self.serializer_class(passport)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, passport_id):

        try:
            passport = Passport.objects.get(id=passport_id)
        except Passport.DoesNotExist as e:
            raise exceptions.APIException(detail=e, code=404)

        serializer_data = request.data

        serializer = self.serializer_class(
            passport, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, passport_id):

        try:
            passport = Passport.objects.get(id=passport_id)
        except User.DoesNotExist as e:
            raise exceptions.APIException(detail=e, code=404)

        passport.delete()

        return Response({}, status=status.HTTP_200_OK)
