from django.urls import path
from . import views

urlpatterns = [
    path(
        "list/",
        views.CarsListView.as_view(),
        name="list_cars",
    ),
    path(
        "add/",
        views.CarsAddView.as_view(),
        name="add_cars",
    ),
    path(
        "search/",
        views.CarSearchView.as_view(),
        name="search_car",
    ),
    path(
        "update/",
        views.CarUpdateView.as_view(),
        name="update_car",
    ),
    path(
        "delete/",
        views.CarDeleteView.as_view(),
        name="delete_car",
    ),
]
