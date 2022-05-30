from django.urls import path

from .views import (
    RegistrationAPIView, AuthenticationAPIView, UserRetrieveUpdateAPIView,
    UsersRetrieveAPIView, UserAdminAPIView, PassportsApiView, PassportAPIView
)


app_name = 'small_app'
urlpatterns = [
    path('users', RegistrationAPIView.as_view()),
    path('login', AuthenticationAPIView.as_view()),
    path('users/current', UserRetrieveUpdateAPIView.as_view()),
    path('users_search', UsersRetrieveAPIView.as_view()),
    path('users/<int:user_id>', UserAdminAPIView.as_view()),
    path('passports', PassportsApiView.as_view()),
    path('passports/<int:passport_id>', PassportAPIView.as_view())
]