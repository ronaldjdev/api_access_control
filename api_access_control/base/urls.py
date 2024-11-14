"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from register_access.api.viewset import GenerateQrCodeViewSet
from register_access.views import verify_qr, generate_qr_from_employee, generate_qr_temporary
from user.views import SignInView, LogoutView, RefreshTokenView, RegisterView, TokenVerifyView, SendEmailView
from user.api.router import router as user_router

schema_view = get_schema_view(
    openapi.Info(
        title="Access Control API",
        default_version="v1",
        description="Documentación de la API para el sistema de control de acceso",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api-auth', include('rest_framework.urls')),
    path('api/', include(user_router.urls)),

    # Generacion y verificacion de QR
    # path('generar-qr', GenerateQrCodeViewSet.as_view(), name='generate_qr'),
    path('verify-qr', verify_qr, name='verify_qr'),
    path('generate-qr', generate_qr_from_employee, name='generate_qr_from_employee'),
    path('generate-qr-view', generate_qr_temporary, name='generate_qr'),

    # Auth
    path('sign-in', SignInView.as_view(), name='sign_in'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('refresh', RefreshTokenView.as_view(), name='refresh'),
    path('register', RegisterView.as_view(), name='register'),
    path('token-verify', TokenVerifyView.as_view(), name='token_verify'),

    # Email
    path('send-email', SendEmailView.as_view(), name='send_email'),

    # Swagger
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
