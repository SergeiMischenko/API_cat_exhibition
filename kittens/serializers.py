from rest_framework import serializers

from kittens.models import Breed, Kitten, Rating


class BreedSerializer(serializers.ModelSerializer):
    """Сериализатор для пород котиков"""

    class Meta:
        model = Breed
        fields = ["id", "name"]


class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга котиков"""

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Rating
        fields = ["user", "rating"]


class KittenSerializer(serializers.ModelSerializer):
    """Сериализатор для котиков"""

    breed = BreedSerializer(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Kitten
        fields = [
            "id",
            "breed",
            "color",
            "age",
            "description",
            "owner",
            "average_rating",
        ]


class KittenDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра котиков"""

    breed = BreedSerializer(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    ratings = RatingSerializer(source="rating_kitten", many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Kitten
        fields = [
            "id",
            "breed",
            "color",
            "age",
            "description",
            "owner",
            "average_rating",
            "ratings",
        ]


class KittenCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/изменения котиков"""

    class Meta:
        model = Kitten
        fields = ["breed", "color", "age", "description", "owner"]
