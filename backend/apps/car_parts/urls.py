from django.urls import path
from . import views

urlpatterns = [
    path(
        "list/",
        views.PartsListView.as_view(),
        name="list_parts",
    ),
    path(
        "add/",
        views.PartAddView.as_view(),
        name="add_part",
    ),
    path(
        "search/",
        views.PartSearchView.as_view(),
        name="search_part",
    ),
    path(
        "update/",
        views.PartUpdateView.as_view(),
        name="update_part",
    ),
    path(
        "delete/",
        views.PartDeleteView.as_view(),
        name="delete_part",
    ),
]
