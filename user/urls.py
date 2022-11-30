from rest_framework import routers
from .api import RegistrationAPIView, LoginAPIView, UserView

router = routers.DefaultRouter()
router.register('user/login', LoginAPIView, 'user-login')
router.register('user', UserView, 'user')
router.register('user/registration', RegistrationAPIView, 'user-registration')

urlpatterns = router.urls