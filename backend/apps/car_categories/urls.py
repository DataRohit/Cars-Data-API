from django.urls import path
from . import views

urlpatterns = [
    path(
        "list/",
        views.CarCategoryListView.as_view(),
        name="list_car_categories",
    ),
    path(
        "add/",
        views.CarCategoryAddView.as_view(),
        name="add_car_categories",
    ),
    path(
        "search/",
        views.CarCategorySearchView.as_view(),
        name="search_car_categories",
    ),
    path(
        "update/",
        views.CarCategoryUpdateView.as_view(),
        name="update_car_categories",
    ),
    path(
        "delete/",
        views.CarCategoryDeleteView.as_view(),
        name="delete_car_categories",
    ),
]
