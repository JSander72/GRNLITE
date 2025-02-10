import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta, timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile, CustomUser, UserToken
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        try:
            # Ensure the profile is created for the user
            if not Profile.objects.filter(user=instance).exists():
                Profile.objects.create(
                    user=instance,
                    user_type=instance.user_type,
                    bio="This is your default bio.",
                )
                logger.debug(f"Profile created for user: {instance.username}")
        except Exception as e:
            logger.error(f"Error creating profile for user {instance.username}: {e}")
    else:
        try:
            if hasattr(instance, "profile"):
                instance.profile.user_type = instance.user_type
                instance.profile.save()
                logger.debug(f"Profile updated for user: {instance.username}")
        except Exception as e:
            logger.error(f"Error updating profile for user {instance.username}: {e}")

    # JWT token generation
    try:
        token = jwt.encode(
            {
                "user_id": instance.id,
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        logger.debug(f"JWT token generated for user: {instance.username} -> {token}")
    except PyJWTError as e:  # Generic JWT error handling
        logger.error(f"Error generating JWT token for user {instance.username}: {e}")
    except Exception as e:  # Fallback for other unexpected errors
        logger.error(f"Unexpected error during token generation: {e}")


@receiver(post_save, sender=CustomUser)
def create_or_update_profile_and_token(sender, instance, created, **kwargs):
    if created:
        try:
            # Ensure the profile is created only once
            Profile.objects.get_or_create(
                user=instance, defaults={"user_type": instance.user_type}
            )

            # Generate and save JWT token
            token = jwt.encode(
                {
                    "user_id": instance.id,
                    "exp": datetime.now(timezone.utc) + timedelta(days=1),
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            print(f"User Type for created Profile: {instance.user_type}")

            # Save the token in UserToken table
            UserToken.objects.create(user=instance, token=token)
        except Exception as e:
            logger.error(
                f"Error during profile or token creation for user {instance.username}: {e}"
            )
