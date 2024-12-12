from rest_framework.routers import DefaultRouter
from .views import PostSerializerViewSet

router = DefaultRouter()
router.register(r'posts', PostSerializerViewSet, basename='posts')

urlpatterns = router.urls