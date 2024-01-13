from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Car Dealership API",
        default_version="v1",
        description="A Car Dealership API",
        contact=openapi.Contact(email="rohit.vilas.ingole@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls, name="admin"),
    path("", include("backend.apps.home.urls")),
    path("jwtauth/", include("backend.apps.jwtauth.urls")),
    path("cars/", include("backend.apps.cars.urls")),
    path("car_categories/", include("backend.apps.car_categories.urls")),
    path("car_parts/", include("backend.apps.car_parts.urls")),
]
