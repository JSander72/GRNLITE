from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Profile


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Verify your account",
            "Click the link to verify your account: http://example.com/verify",
            "from@example.com",
            [instance.email],
            fail_silently=False,
        )


@receiver(user_logged_in)
def redirect_after_login(sender, user, request, **kwargs):
    # Redirect logic here
    if not hasattr(user, "profile"):
        # Handle missing profile gracefully
        return redirect("profile_setup")  # Redirect to a profile setup page if needed
    if user.profile.user_type == "author":
        return redirect("author_dashboard")
    return redirect("reader_dashboard")


@receiver(user_logged_out)
def redirect_after_logout(sender, user, request, **kwargs):
    return redirect("home")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()
