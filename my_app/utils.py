from django.contrib.auth import get_user_model


def get_or_create_user(email, defaults):
    User = get_user_model()
    user, created = User.objects.get_or_create(email=email, defaults=defaults)
    return user
