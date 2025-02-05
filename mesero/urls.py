"""
URL configuration for mesero project.

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
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Crear una vista de esquema para Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API de Mesero",
        default_version='v1',
        description="Documentación de la API de nuestro sistema",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@mesero.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('api/', include('mesero.presentation.urls')),  # Incluye las rutas de `presentation`
]


