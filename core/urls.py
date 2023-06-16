from django.urls import path

from .views import (
    RegisterAPIView, LoginAPIView, UserAPIView, LogoutAPIView,
    ProfileInfoAPIView, ProfilePasswordAPIView,UserDeleteAPIView,
    UsersListAPIView,GoogleSocialAuthView
)

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),
    path('user/delete/<int:pk>',UserDeleteAPIView.as_view()),
    path('usersList',UsersListAPIView.as_view()),

    path('google/', GoogleSocialAuthView.as_view()),
]

