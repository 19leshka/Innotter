from rest_framework import routers
from .api import UserViewSet, RegistrationAPIView

# router = routers.DefaultRouter()
# router.register('user/', RegistrationAPIView.as_view(), 'user-registration')
# # router.register('api/user', UserViewSet, 'user')
#
# urlpatterns = router.urls