from rest_framework.routers import DefaultRouter

from .viewset import RegisterAccessViewSet

router = DefaultRouter()
router.register(prefix='registro_acesso',viewset=RegisterAccessViewSet)