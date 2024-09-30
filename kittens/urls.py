from django.urls import path

from kittens.views import (BreedListView, KittenDetailUpdateDestroyView,
                           KittenListCreateView, RatingCreateView)

urlpatterns = [
    path("", KittenListCreateView.as_view(), name="kitten_list_create"),
    path(
        "<int:pk>/",
        KittenDetailUpdateDestroyView.as_view(),
        name="kitten_detail_update_delete",
    ),
    path("<int:pk>/rate/", RatingCreateView.as_view(), name="kitten_rate"),
    path("breeds/", BreedListView.as_view(), name="breed_list_create"),
]
