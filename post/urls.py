from rest_framework import routers

from .api import PostView

router = routers.DefaultRouter()
router.register('posts', PostView, 'posts')

urlpatterns = router.urls
