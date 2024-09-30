from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Breed(models.Model):
    """Модель для пород котиков"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Порода")

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Kitten(models.Model):
    """Модель для котиков"""

    breed = models.ForeignKey(
        Breed, on_delete=models.CASCADE, verbose_name="Порода", related_name="kittens"
    )
    color = models.CharField(max_length=50, verbose_name="Цвет")
    age = models.PositiveSmallIntegerField(verbose_name="Возраст (месяцев)")
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="kitten_owner",
    )

    class Meta:
        verbose_name = "Котенок"
        verbose_name_plural = "Котята"
        ordering = ["age"]
        indexes = [
            models.Index(fields=["age"]),
        ]

    def __str__(self):
        return f"{self.color} котенок, {self.age} месяцев породы {self.breed}"


class Rating(models.Model):
    """Модель для рейтинга котиков"""

    kitten = models.ForeignKey(
        Kitten,
        on_delete=models.CASCADE,
        verbose_name="Котенок",
        related_name="rating_kitten",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="rating_user",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Рейтинг"
    )

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        ordering = ["-rating"]
        unique_together = ("kitten", "user")
        indexes = [
            models.Index(fields=["-rating"]),
        ]

    def __str__(self):
        return f"{self.rating} баллов для {self.kitten} от {self.user}"
