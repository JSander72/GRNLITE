from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from my_app.models import Profile


class Command(BaseCommand):
    help = "Create profiles for users without one"

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
        self.stdout.write(
            f"Created profiles for {users_without_profiles.count()} users."
        )
