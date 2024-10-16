from rest_framework.routers import DefaultRouter

from .viewset import EmployeeViewSet
from register_access.api.viewset import RegisterAccessViewSet

router = DefaultRouter()
router.register(prefix='empleado',viewset=EmployeeViewSet)
router.register(prefix='registro_acesso',viewset=RegisterAccessViewSet)