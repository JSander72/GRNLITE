from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from my_app.models import Profile, CustomUser
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
import logging
from django.db import transaction


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
        # Create the profile (ensure defaults are meaningful)
        # Use on_commit to ensure the user is fully saved in the database
        transaction.on_commit(
            lambda: Profile.objects.create(user=instance, user_type="default")
        )
        if created:
            logger.debug(f"Profile created for user: {instance.username}")

        else:
            logger.debug(f"Profile already exists for user: {instance.username}")

        # Generate a JWT token
        token = jwt.encode(
            {
                "user_id": instance.id,
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        # Log or return the token (based on use case)
        logger.debug(f"JWT Token for {instance.username}: {token}")
