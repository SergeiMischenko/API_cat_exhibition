import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from kittens.models import Breed, Kitten
from kittens.serializers import (KittenCreateUpdateSerializer,
                                 KittenSerializer, RatingSerializer)

User = get_user_model()


@pytest.fixture
def breed():
    return Breed.objects.create(name="Сиамская")


@pytest.fixture
def regular_user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def kitten(breed, regular_user):
    return Kitten.objects.create(
        breed=breed,
        color="Серый",
        age=5,
        description="Очень игривый котёнок",
        owner=regular_user,
    )


@pytest.mark.django_db
def test_kitten_serializer(breed):
    """Проверка сериализатора для котиков"""
    kitten_data = {
        "breed": breed.id,
        "color": "Серый",
        "age": 5,
        "description": "Очень игривый котёнок",
    }
    serializer = KittenSerializer(data=kitten_data)
    assert serializer.is_valid()
    assert serializer.validated_data["color"] == "Серый"
    assert serializer.validated_data["age"] == 5
    assert serializer.validated_data["description"] == "Очень игривый котёнок"


@pytest.mark.django_db
def test_kitten_create_serializer(breed, regular_user):
    """Проверка сериализатора для создания котиков"""
    kitten_data = {
        "breed": breed.id,
        "color": "Серый",
        "age": 5,
        "description": "Очень игривый котёнок",
    }
    serializer = KittenCreateUpdateSerializer(data=kitten_data)
    assert serializer.is_valid(), serializer.errors
    kitten = serializer.save(owner=regular_user)
    assert kitten.breed.name == "Сиамская"
    assert kitten.color == "Серый"
    assert kitten.age == 5
    assert kitten.description == "Очень игривый котёнок"
    assert kitten.owner == regular_user


@pytest.mark.django_db
def test_invalid_kitten_create_serializer(breed):
    """Проверка сериализатора для создания котиков с невалидными данными"""
    kitten_data = {
        "breed": breed.id,
        "color": "",  # Пустое поле color
        "age": -1,  # Неверное значение возраста
        "description": "Очень игривый котёнок",
    }
    serializer = KittenCreateUpdateSerializer(data=kitten_data)
    with pytest.raises(ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)

    assert "color" in exc_info.value.detail
    assert "age" in exc_info.value.detail


@pytest.mark.django_db
def test_rating_serializer(regular_user):
    """Проверка сериализатора рейтинга"""
    rating_data = {
        "user": regular_user,
        "rating": 4,
    }
    serializer = RatingSerializer(data=rating_data)
    assert serializer.is_valid()
    assert serializer.validated_data["rating"] == 4


@pytest.mark.django_db
def test_invalid_rating(regular_user):
    """Проверка невалидного рейтинга"""
    rating_data = {
        "user": regular_user,
        "rating": 6,
    }
    serializer = RatingSerializer(data=rating_data)
    with pytest.raises(ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)

    assert "rating" in exc_info.value.detail
