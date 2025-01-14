from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.signals import user_logged_in, user_logged_out
from my_app.models import Profile, CustomUser


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


@receiver(user_logged_in, sender=CustomUser)
def redirect_after_login(sender, user, request, **kwargs):
    # Skip redirection for admin login
    if request.path.startswith("/admin/"):
        return

    # Check if user has a profile and determine redirection based on user_type
    if not hasattr(user, "profile"):
        # Ensure the user belongs to the correct model
        if isinstance(user, CustomUser):
            Profile.objects.create(user=user)

        if user.profile.user_type == "reader":
            return redirect("reader-dashboard")  # Redirect to reader dashboard
        elif user.profile.user_type == "author":
            return redirect("author-dashboard")  # Redirect to author dashboard

    # Default case if no profile or user_type, redirect to the home page
    return redirect(
        "my_app:home"
    )  # This will now correctly use the home route to render main.html


@receiver(user_logged_out)
def redirect_after_logout(sender, user, request, **kwargs):
    # Skip redirection for admin logout
    if request.path.startswith("/admin/"):
        return
    return redirect("my_app:home")  # Redirect to home page after logout


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, user_type="default")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()
