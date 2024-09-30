from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Breed, Kitten, Rating


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Kitten)
class KittenAdmin(admin.ModelAdmin):
    list_display = ("breed", "color", "age", "owner")
    list_filter = ("breed", "color", "age")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("kitten_link", "user", "rating")
    list_filter = ("kitten", "user", "rating")

    @admin.display(description="Котенок")
    def kitten_link(self, obj):
        url = reverse("admin:kittens_kitten_change", args=(obj.kitten.id,))
        return format_html('<a href="{}">{}</a>', url, obj.kitten)
