"""
Management command to clean up expired email verification codes.
"""

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from my_app.models import EmailVerification


class Command(BaseCommand):
    help = "Clean up expired email verification codes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)

        # Find expired verification codes
        expired_verifications = EmailVerification.objects.filter(
            expires_at__lt=now(), is_used=False
        )

        count = expired_verifications.count()

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"DRY RUN: Would mark {count} expired verification codes as used."
                )
            )
            for verification in expired_verifications[:10]:  # Show first 10
                self.stdout.write(
                    f"- {verification.email} (expired at {verification.expires_at})"
                )
            if count > 10:
                self.stdout.write(f"... and {count - 10} more")
        else:
            if count == 0:
                self.stdout.write(
                    self.style.SUCCESS("No expired verification codes found.")
                )
            else:
                expired_verifications.update(is_used=True)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Marked {count} expired verification codes as used."
                    )
                )
