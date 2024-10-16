from rest_framework.routers import DefaultRouter

from .viewset import EmployeeViewSet

router = DefaultRouter()
router.register(prefix='empleado',viewset=EmployeeViewSet)