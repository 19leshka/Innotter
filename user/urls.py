from rest_framework import routers
from .api import RegistrationAPIView, LoginAPIView

router = routers.DefaultRouter()
router.register('user/login', LoginAPIView, 'user-login')
router.register('user', RegistrationAPIView, 'user-registration')

urlpatterns = router.urls