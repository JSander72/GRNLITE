from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from my_app.models import Profile, CustomUser
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
import logging
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()


# Send verification email after user is created
@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Verify your account",
            "Click the link to verify your account: http://example.com/verify",
            "from@example.com",
            [instance.email],
            fail_silently=False,
        )


logger = logging.getLogger(__name__)


# Create a profile and JWT token after user creation
@receiver(post_save, sender=CustomUser)
def create_user_dependencies(sender, instance, created, **kwargs):
    if created:
        try:
            # Ensure that the profile is created only if it doesn't exist
            transaction.on_commit(
                lambda: Profile.objects.create(
                    user=instance, user_type=instance.user_type
                )
            )
            logger.debug(f"Profile created for user: {instance.username}")
        except Exception as e:
            logger.error(f"Error creating profile for user {instance.username}: {e}")
    else:
        try:
            # Optionally update the profile if it exists or if you want to perform some other action
            if hasattr(instance, "profile"):
                logger.debug(f"Profile already exists for user: {instance.username}")
            else:
                # In case there is no profile, you can create one here too
                Profile.objects.create(user=instance, user_type=instance.user_type)
        except Exception as e:
            logger.error(f"Error updating profile for user {instance.username}: {e}")

    try:
        # Generate a JWT token
        token = jwt.encode(
            {
                "user_id": instance.id,
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        logger.debug(f"JWT token generated for user: {instance.username}")
    except Exception as e:
        logger.error(f"Error generating JWT token for user {instance.username}: {e}")


@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile when a new CustomUser is created
        Profile.objects.create(user=instance, user_type=instance.user_type)
        logger.info(f"Profile created for user: {instance.username}")
    else:
        # Optionally update the profile if necessary
        if hasattr(instance, "profile"):
            instance.profile.save()
            logger.info(f"Profile updated for user: {instance.username}")
