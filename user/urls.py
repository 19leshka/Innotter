from rest_framework import routers
from user.api import AuthAPIView, UserView

router = routers.DefaultRouter()
router.register('user', UserView, 'user')
router.register('auth', AuthAPIView, 'user-auth')

urlpatterns = router.urls