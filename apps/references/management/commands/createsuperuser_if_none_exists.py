import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create superuser if not exist"

    def handle(self, *args, **options):
        user_model = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")

        if not username or not password or not email:
            raise CommandError(
                "DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD "
                "and DJANGO_SUPERUSER_EMAIL must be set"
            )

        if not user_model.objects.filter(username=username).exists():
            self.stdout.write(f"Creating superuser with username: {username}")
            user_model.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        else:
            self.stdout.write(f"Superuser {username} already exists.")
