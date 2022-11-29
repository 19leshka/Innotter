from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from user.api import LoginAPIView, RegistrationAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('user.urls')),
    path('api/user/', RegistrationAPIView.as_view()),
    path('api/user/login/', LoginAPIView.as_view()),
]