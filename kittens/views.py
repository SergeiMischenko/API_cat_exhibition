from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from kittens.models import Breed, Kitten, Rating
from kittens.permissions import IsAuthorOrReadOnly
from kittens.serializers import (BreedSerializer, KittenCreateUpdateSerializer,
                                 KittenDetailSerializer, KittenSerializer,
                                 RatingSerializer)


class BreedListView(ListCreateAPIView):
    """Получение списка пород"""

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return []


class KittenListCreateView(ListCreateAPIView):
    """Получение списка котиков и создание нового котика"""

    queryset = Kitten.objects.annotate(average_rating=Avg("rating_kitten__rating"))
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["breed", "color", "age"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return KittenCreateUpdateSerializer
        return KittenSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class KittenDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Получение, изменение и удаление котика"""

    queryset = Kitten.objects.annotate(average_rating=Avg("rating_kitten__rating"))
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return KittenDetailSerializer
        return KittenCreateUpdateSerializer


class RatingCreateView(ListCreateAPIView):
    """Добавление рейтинга котику"""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        kitten = get_object_or_404(Kitten, id=self.kwargs["pk"])
        serializer.save(user=self.request.user, kitten=kitten)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []
