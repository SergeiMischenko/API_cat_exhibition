import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from kittens.models import Breed, Kitten

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def superuser(api_client):
    user = User.objects.create_superuser(username="admin", password="password")
    api_client.force_authenticate(user=user)
    return user, api_client


@pytest.fixture
def regular_user(api_client):
    user = User.objects.create_user(username="testuser", password="password")
    api_client.force_authenticate(user=user)
    return user, api_client


@pytest.fixture
def breed():
    return Breed.objects.create(name="Сиамская")


@pytest.fixture
def kitten(regular_user, breed):
    user, _ = regular_user
    return Kitten.objects.create(
        breed=breed, color="Серый", age=5, description="Игривый кот", owner=user
    )


@pytest.mark.django_db
def test_breed_create_without_auth(api_client):
    """Проверка создания породы без авторизации"""
    breed_data = {"name": "Сиамская"}
    response = api_client.post("/api/breeds/", breed_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_breed_create_not_superuser(regular_user, api_client):
    """Проверка создания породы обычным пользователем"""
    breed_data = {"name": "Сиамская"}
    response = api_client.post("/api/breeds/", breed_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_breed_list_view(superuser):
    """Проверка получения списка пород котиков"""
    _, api_client = superuser

    breed_data = {"name": "Сиамская"}
    response = api_client.post("/api/breeds/", breed_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] == 1
    assert response.data["name"] == "Сиамская"

    response = api_client.get("/api/breeds/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == 1
    assert response.data["results"][0]["name"] == "Сиамская"


@pytest.mark.django_db
def test_breed_creation_unique_name(superuser):
    """Проверка создания породы с уже существующим именем"""
    _, api_client = superuser

    breed_data = {"name": "Сиамская"}
    response = api_client.post("/api/breeds/", breed_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = api_client.post("/api/breeds/", breed_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_kitten_list_create_view(regular_user, breed, api_client):
    """Проверка получения списка котиков и создания котенка"""
    user, _ = regular_user

    kitten_data = {
        "breed": breed.id,
        "color": "Серый",
        "age": 5,
        "description": "Очень игривый котёнок",
    }
    response = api_client.post("/api/", kitten_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["breed"] == 1
    assert response.data["color"] == "Серый"
    assert response.data["age"] == 5
    assert response.data["description"] == "Очень игривый котёнок"

    response = api_client.get("/api/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["breed"]["name"] == "Сиамская"
    assert response.data["results"][0]["color"] == "Серый"
    assert response.data["results"][0]["age"] == 5
    assert response.data["results"][0]["description"] == "Очень игривый котёнок"


@pytest.mark.django_db
def test_kitten_detail_update_destroy_view(regular_user, kitten, api_client):
    """Проверка получения котенка, обновления котенка и удаления котенка"""
    user, _ = regular_user

    response = api_client.get(f"/api/{kitten.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["color"] == "Серый"
    assert response.data["age"] == 5
    assert response.data["description"] == "Игривый кот"

    updated_data = {
        "breed": kitten.breed.id,
        "color": "Белый",
        "age": 6,
        "description": "Другой игривый котёнок",
    }
    response = api_client.put(f"/api/{kitten.id}/", updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["color"] == "Белый"
    assert response.data["age"] == 6
    assert response.data["description"] == "Другой игривый котёнок"

    response = api_client.delete(f"/api/{kitten.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = api_client.get(f"/api/{kitten.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
