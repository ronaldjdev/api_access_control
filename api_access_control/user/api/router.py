from rest_framework.routers import DefaultRouter

from employee.api.viewset import EmployeeViewSet
from register_access.api.viewset import RegisterAccessViewSet, GenerateQrCodeViewSet
from .viewset import UserViewSet


router = DefaultRouter()
router.register(prefix='empleado',viewset=EmployeeViewSet)
router.register(prefix='registro_acesso',viewset=RegisterAccessViewSet)
router.register(prefix='usuario',viewset=UserViewSet)
router.register(prefix='generar-qr',viewset=GenerateQrCodeViewSet)