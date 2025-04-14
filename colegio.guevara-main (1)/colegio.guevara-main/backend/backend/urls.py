"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

from core.views import (
    UserProfileView,
    MateriaListView,
    NotasPorAlumnoView,
    CursadaPorAlumnoView,
    CrearNotaView
)



# 📌 Configuración del esquema de la API
schema_view = get_schema_view(
    openapi.Info(
        title="API de Boletines",
        default_version='v1',
        description="Documentación de la API del sistema de boletines",
        terms_of_service="https://www.tusitio.com/terminos/",
        contact=openapi.Contact(email="contacto@tusitio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # 📌 Swagger en formato UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # 📌 Documentación en formato Redoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # 📌 Documentación en formato JSON y YAML
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),

    # 📌 Autenticación con JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 📌 Perfil de usuario autenticado
    path('api/user/', UserProfileView.as_view(), name='user_profile'),

    # 📌 Materias
    path('api/materias/', MateriaListView.as_view(), name='materias_list'),

    # 📌 Notas por alumno y año
    path('api/notas/<int:alumno_id>/<int:anio>/', NotasPorAlumnoView.as_view(), name='notas_por_alumno'),

    # 📌 Cursada por alumno
    path('api/cursada/<int:alumno_id>/', CursadaPorAlumnoView.as_view(), name='cursada_por_alumno'),

    # 📌 Crear una nueva nota
    path('api/notas/nueva/', CrearNotaView.as_view(), name='crear_nota'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from core.views import generar_grafico_view

urlpatterns += [
    path("generar-grafico/<int:alumno_id>/", generar_grafico_view, name="generar_grafico"),
]