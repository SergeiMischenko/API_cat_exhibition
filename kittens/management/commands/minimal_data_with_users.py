from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from kittens.models import Breed, Kitten, Rating

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users, breeds, kittens, and ratings'

    def handle(self, *args, **kwargs):
        # Создаем пользователей
        user1 = User.objects.create_user(username='user1')
        user1.set_password('user1')
        user1.save()

        user2 = User.objects.create_user(username='user2')
        user2.set_password('user2')
        user2.save()

        # Создаем суперпользователя
        admin = User.objects.create_superuser(username='admin', password='admin')
        admin.save()

        # Создаем породы
        breed1 = Breed.objects.create(name='Сиамская')
        breed2 = Breed.objects.create(name='Британская')
        breed3 = Breed.objects.create(name='Мейн-кун')

        # Создаем котят
        kitten1 = Kitten.objects.create(
            breed=breed1, color='Серый', age=4, description='Очень игривый котёнок', owner=user1
        )
        kitten2 = Kitten.objects.create(
            breed=breed2, color='Черный', age=6, description='Спокойный котёнок', owner=user2
        )
        kitten3 = Kitten.objects.create(
            breed=breed3, color='Белый', age=3, description='Любопытный котёнок', owner=user1
        )

        # Создаем рейтинги
        Rating.objects.create(kitten=kitten1, user=user1, rating=5)
        Rating.objects.create(kitten=kitten1, user=user2, rating=2)
        Rating.objects.create(kitten=kitten3, user=user1, rating=4)

        self.stdout.write(self.style.SUCCESS('Users, breeds, kittens, and ratings created successfully'))
