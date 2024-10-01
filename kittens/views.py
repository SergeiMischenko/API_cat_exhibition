from django.db.models import Avg
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from kittens.models import Breed, Kitten, Rating
from kittens.permissions import IsAuthorOrReadOnly
from kittens.serializers import (BreedSerializer, KittenCreateUpdateSerializer,
                                 KittenDetailSerializer, KittenSerializer,
                                 RatingSerializer)


@extend_schema_view(
    get=extend_schema(
        tags=["Breeds"],
        summary="Получение списка пород котиков",
        description="Возвращает список всех пород котиков.",
        responses=BreedSerializer(many=True),
    ),
    post=extend_schema(
        tags=["Breeds"],
        summary="Создание новой породы котика",
        description="Создает новую породу котика и возвращает ее данные. Доступно только администраторам.",
    ),
)
class BreedListView(ListCreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return super().get_permissions()


@extend_schema_view(
    get=extend_schema(
        tags=["Kittens"],
        summary="Получение списка котиков",
        description="Возвращает список всех котиков, фильтрация по породе, пагинация.",
        responses=KittenSerializer(many=True),
    ),
    post=extend_schema(
        tags=["Kittens"],
        summary="Создание нового котика",
        description="Создает нового котика и возвращает его данные. Требуется авторизация.",
        request=KittenCreateUpdateSerializer,
        responses=KittenSerializer,
    ),
)
class KittenListCreateView(ListCreateAPIView):
    queryset = Kitten.objects.annotate(
        average_rating=Avg("rating_kitten__rating")
    ).order_by("id")
    filterset_fields = ["breed"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return KittenCreateUpdateSerializer
        return KittenSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema_view(
    get=extend_schema(
        tags=["Kittens {id}"],
        summary="Получение одного котика",
        description="Возвращает данные одного котика.",
    ),
    put=extend_schema(
        tags=["Kittens {id}"],
        summary="Изменение котика (полностью)",
        description="Изменяет данные котика. Требуется авторизация (только автор или администратор).",
    ),
    patch=extend_schema(
        tags=["Kittens {id}"],
        summary="Изменение котика (частично)",
        description="Изменяет данные котика. Требуется авторизация (только автор или администратор).",
    ),
    delete=extend_schema(
        tags=["Kittens {id}"],
        summary="Удаление котика",
        description="Удаляет котика. Требуется авторизация (только автор или администратор).",
    ),
)
class KittenDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Kitten.objects.annotate(average_rating=Avg("rating_kitten__rating"))
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return KittenDetailSerializer
        return KittenCreateUpdateSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["Ratings {id}"],
        summary="Добавление рейтинга котику",
        description="Добавляет рейтинг котику. Требуется авторизация.",
    ),
)
class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        kitten = get_object_or_404(Kitten, id=self.kwargs["pk"])
        serializer.save(user=self.request.user, kitten=kitten)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication (JWT)"],
        summary="Получение токена доступа",
        description="Возвращает токен доступа и токен обновления для аутентификации пользователя.",
    ),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication (JWT)"],
        summary="Обновление токена доступа",
        description="Обновляет токен доступа, используя токен обновления.",
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
