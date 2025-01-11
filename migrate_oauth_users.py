import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "my_app.settings"
)  # Replace with your project settings
import django

django.setup()

from django.contrib.auth.models import User


def migrate_users():
    # Example data to simulate user migration
    users_data = [
        {
            "username": "user1",
            "email": "user1@example.com",
            "first_name": "User",
            "last_name": "One",
        },
        {
            "username": "user2",
            "email": "user2@example.com",
            "first_name": "User",
            "last_name": "Two",
        },
    ]

    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={
                "email": user_data["email"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
            },
        )
        if not created:
            # Update existing User (if needed)
            if not user.email and user_data.get("email"):
                user.email = user_data["email"]
                user.save()


if __name__ == "__main__":
    migrate_users()
