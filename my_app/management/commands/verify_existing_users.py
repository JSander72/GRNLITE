"""
Management command to verify all existing users' emails for development/testing.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class Command(BaseCommand):
    help = "Mark all existing users as email verified for development/testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Verify email for a specific username only",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force verification even if already verified",
        )

    def handle(self, *args, **options):
        username = options.get("username")
        force = options.get("force", False)

        if username:
            try:
                user = User.objects.get(username=username)
                users = [user]
                self.stdout.write(f"Processing user: {username}")
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User '{username}' not found."))
                return
        else:
            if force:
                users = User.objects.all()
            else:
                users = User.objects.filter(is_email_verified=False)
            self.stdout.write(f"Processing {users.count()} users...")

        verified_count = 0
        for user in users:
            if not user.is_email_verified or force:
                user.is_email_verified = True
                user.email_verified_at = now()
                user.is_active = True
                user.save()
                verified_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Verified email for: {user.username}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"- Already verified: {user.username}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"\nCompleted! Verified {verified_count} user(s).")
        )
