from django.db.models.signals import post_save
from django.dispatch import receiver
from my_app.models import Profile, CustomUser
import jwt
from jwt.exceptions import PyJWTError  # Correct base exception for PyJWT
from datetime import datetime, timedelta, timezone
from django.conf import settings
import logging
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)


# Create a profile and JWT token after user creation
@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        try:
            # Ensure the profile is created for the user
            if not Profile.objects.filter(user=instance).exists():
                Profile.objects.create(user=instance, user_type=instance.user_type)
                logger.debug(f"Profile created for user: {instance.username}")
        except Exception as e:
            logger.error(f"Error creating profile for user {instance.username}: {e}")
    else:
        try:
            # Ensure profile exists and is updated if needed
            if hasattr(instance, "profile"):
                instance.profile.save()
                logger.debug(f"Profile updated for user: {instance.username}")
            else:
                Profile.objects.create(user=instance, user_type=instance.user_type)
                logger.debug(f"Profile created for user: {instance.username}")
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
        logger.debug(f"JWT token generated for user: {instance.username}")
    except PyJWTError as e:  # Correctly handle PyJWT exceptions
        logger.error(f"Error generating JWT token for user {instance.username}: {e}")
