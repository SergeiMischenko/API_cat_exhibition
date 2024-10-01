from django.core.validators import MaxValueValidator, MinValueValidator
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

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    class Meta:
        model = Rating
        fields = ["user", "rating"]


class BaseKittenSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для котиков"""

    breed = BreedSerializer(read_only=True)
    age = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(255)],
    )
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


class KittenSerializer(BaseKittenSerializer):
    """Сериализатор для котиков"""

    class Meta(BaseKittenSerializer.Meta):
        pass


class KittenDetailSerializer(BaseKittenSerializer):
    """Сериализатор для детального просмотра котиков"""

    ratings = RatingSerializer(source="rating_kitten", many=True, read_only=True)

    class Meta(BaseKittenSerializer.Meta):
        fields = BaseKittenSerializer.Meta.fields + ["ratings"]


class KittenCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/изменения котиков"""

    breed = serializers.PrimaryKeyRelatedField(queryset=Breed.objects.all())
    age = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(255),
        ],
        default=1,
    )

    def validate_age(self, value):
        if value < 1:
            raise serializers.ValidationError("Возраст должен быть не менее 1 месяца.")
        return value

    class Meta:
        model = Kitten
        fields = ["breed", "color", "age", "description"]
        read_only_fields = ["owner"]
