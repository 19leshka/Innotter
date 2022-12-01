from rest_framework import routers

from .api import PagesView

router = routers.DefaultRouter()
router.register('pages', PagesView, 'pages')

urlpatterns = router.urls