from rest_framework import routers
from .api import RegistrationAPIView, LoginAPIView, UserView

router = routers.DefaultRouter()
router.register('user/registration', RegistrationAPIView, 'user-registration')
router.register('user/login', LoginAPIView, 'user-login')
router.register('user', UserView, 'user')

urlpatterns = router.urls