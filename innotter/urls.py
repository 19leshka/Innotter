from django.contrib import admin
from django.urls import path, include
from user.api import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', UserRetrieveUpdateAPIView.as_view()),
    path('api/user/', RegistrationAPIView.as_view()),
    path('api/user/login/', LoginAPIView.as_view()),
]