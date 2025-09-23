import json
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
from my_app.models import Profile
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Restore original users from users.json backup to CustomUser model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users-file",
            type=str,
            default="users.json",
            help="Path to the users.json backup file (default: users.json)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without actually creating users",
        )

    def handle(self, *args, **options):
        users_file = options["users_file"]
        dry_run = options["dry_run"]

        # Check if file exists
        if not os.path.exists(users_file):
            raise CommandError(f'Users file "{users_file}" does not exist.')

        # Load the users.json file
        try:
            with open(users_file, "r") as f:
                user_data = json.load(f)
        except json.JSONDecodeError as e:
            raise CommandError(f"Error parsing JSON file: {e}")
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")

        self.stdout.write(f"Found {len(user_data)} users in backup file.")

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for user_entry in user_data:
            if user_entry.get("model") != "auth.user":
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipping non-user entry: {user_entry.get("model")}'
                    )
                )
                continue

            fields = user_entry["fields"]
            username = fields["username"]

            if dry_run:
                self.stdout.write(f"[DRY RUN] Would process user: {username}")
                continue

            # Check if user already exists
            try:
                existing_user = User.objects.get(username=username)
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists. Updating...')
                )
                user = existing_user
                updated_count += 1
            except User.DoesNotExist:
                # Create new user
                user = User(username=username)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Creating user: {username}"))

            # Set user fields
            user.password = fields["password"]  # Already hashed
            user.email = fields["email"]
            user.first_name = fields["first_name"]
            user.last_name = fields["last_name"]
            user.is_staff = fields["is_staff"]
            user.is_active = fields["is_active"]
            user.is_superuser = fields["is_superuser"]

            # Parse and set date_joined
            if fields["date_joined"]:
                user.date_joined = parse_datetime(fields["date_joined"])

            # Parse and set last_login
            if fields["last_login"]:
                user.last_login = parse_datetime(fields["last_login"])

            # Set email verification status
            # Since these are manually verified users, mark them as verified
            user.is_email_verified = True

            # Set user type based on role (default to regular)
            if user.is_superuser:
                user.user_type = "admin"
            elif user.is_staff:
                user.user_type = "staff"
            else:
                user.user_type = "author"  # Default for regular users

            try:
                user.save()

                # Create or update profile
                profile, profile_created = Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        "user_type": user.user_type,
                        "bio": f"Restored user profile for {username}",
                    },
                )

                if not profile_created:
                    profile.user_type = user.user_type
                    profile.save()

                action = "Created" if user.pk and created_count else "Updated"
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{action} user "{username}" (Email: {user.email}, '
                        f"Type: {user.user_type}, Verified: {user.is_email_verified})"
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error saving user "{username}": {e}')
                )
                continue

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"[DRY RUN] Would process {len(user_data)} users from backup."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully processed users: {created_count} created, "
                    f"{updated_count} updated, {skipped_count} skipped."
                )
            )

            # Show current user count
            total_users = User.objects.count()
            self.stdout.write(
                self.style.SUCCESS(f"Total users in database: {total_users}")
            )
