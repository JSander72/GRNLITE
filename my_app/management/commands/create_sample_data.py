from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from my_app.models import (
    Profile,
    Manuscript,
    Genre,
    Keyword,
    FeedbackQuestion,
    BetaReader,
    AuthorSettings,
)
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Create sample data to demonstrate application features"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Creating sample data..."))

        # Get or create user groups
        author_group, _ = Group.objects.get_or_create(name="author")
        beta_reader_group, _ = Group.objects.get_or_create(name="beta_reader")

        # Create sample authors
        sample_authors = [
            {
                "username": "author1",
                "email": "author1@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
            },
            {
                "username": "author2",
                "email": "author2@example.com",
                "first_name": "John",
                "last_name": "Doe",
            },
            {
                "username": "author3",
                "email": "author3@example.com",
                "first_name": "Emily",
                "last_name": "Johnson",
            },
        ]

        authors = []
        for author_data in sample_authors:
            user, created = User.objects.get_or_create(
                username=author_data["username"],
                defaults={
                    "email": author_data["email"],
                    "first_name": author_data["first_name"],
                    "last_name": author_data["last_name"],
                    "user_type": "author",
                },
            )
            if created:
                user.set_password("password123")
                user.save()
                user.groups.add(author_group)
                self.stdout.write(f"Created author: {user.username}")

            # Create author profile if it doesn't exist
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "user_type": "author",
                    "bio": f"{user.first_name} is a passionate writer focusing on creating engaging stories.",
                },
            )

            # Create author settings
            AuthorSettings.objects.get_or_create(
                author=user,
                defaults={
                    "feedback_preferences": {
                        "plot": True,
                        "characters": True,
                        "pacing": True,
                        "dialogue": True,
                    },
                    "notification_preferences": {
                        "email_feedback": True,
                        "email_applications": True,
                    },
                    "profile_visibility": True,
                },
            )

            authors.append(user)

        # Create sample beta readers
        sample_readers = [
            {
                "username": "reader1",
                "email": "reader1@example.com",
                "first_name": "Mike",
                "last_name": "Wilson",
            },
            {
                "username": "reader2",
                "email": "reader2@example.com",
                "first_name": "Sarah",
                "last_name": "Brown",
            },
            {
                "username": "reader3",
                "email": "reader3@example.com",
                "first_name": "David",
                "last_name": "Davis",
            },
            {
                "username": "reader4",
                "email": "reader4@example.com",
                "first_name": "Lisa",
                "last_name": "Garcia",
            },
        ]

        readers = []
        for reader_data in sample_readers:
            user, created = User.objects.get_or_create(
                username=reader_data["username"],
                defaults={
                    "email": reader_data["email"],
                    "first_name": reader_data["first_name"],
                    "last_name": reader_data["last_name"],
                    "user_type": "beta_reader",
                },
            )
            if created:
                user.set_password("password123")
                user.save()
                user.groups.add(beta_reader_group)
                self.stdout.write(f"Created beta reader: {user.username}")

            # Create reader profile
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "user_type": "beta_reader",
                    "bio": f"{user.first_name} is an experienced beta reader with expertise in various genres.",
                },
            )

            # Create beta reader profile
            beta_reader, beta_created = BetaReader.objects.get_or_create(
                user=user,
                defaults={
                    "experience": f"{user.first_name} has been beta reading for 3+ years with expertise in multiple genres. Known for detailed feedback on plot development, character arcs, and pacing."
                },
            )

            # Add some genres to beta reader
            genres = Genre.objects.all()[:4]  # Get first 4 genres
            beta_reader.genres.set(random.sample(list(genres), 2))

            readers.append(user)

        # Create sample manuscripts
        sample_manuscripts = [
            {
                "title": "The Last Beacon",
                "description": "A science fiction thriller about humanity's last hope in a dying universe.",
                "plot_summary": "When Earth's sun begins to die, a small team of scientists discovers an ancient beacon that might hold the key to salvation.",
                "status": "submitted",
                "budget": 500,
                "beta_readers_needed": 3,
            },
            {
                "title": "Whispers in the Fog",
                "description": "A gothic mystery set in Victorian London where nothing is as it seems.",
                "plot_summary": "Detective Inspector Margaret Holmes investigates a series of supernatural murders in the fog-covered streets of London.",
                "status": "in_review",
                "budget": 300,
                "beta_readers_needed": 2,
            },
            {
                "title": "Hearts Across Time",
                "description": "A time-traveling romance that spans centuries.",
                "plot_summary": "A modern-day historian discovers she can travel through time and falls in love with a Renaissance artist.",
                "status": "draft",
                "budget": 400,
                "beta_readers_needed": 4,
            },
            {
                "title": "The Dragon's Heir",
                "description": "An epic fantasy about a young woman who discovers she's the last dragon rider.",
                "plot_summary": "In a world where dragons have been extinct for centuries, Aria discovers she has the rare ability to communicate with the last dragon egg.",
                "status": "submitted",
                "budget": 600,
                "beta_readers_needed": 5,
            },
        ]

        # Get some keywords and genres
        sci_fi_genre = Genre.objects.filter(name="Science Fiction").first()
        fantasy_genre = Genre.objects.filter(name="Fantasy").first()
        romance_genre = Genre.objects.filter(name="Romance").first()
        mystery_genre = Genre.objects.filter(name="Mystery").first()

        adventure_keyword = Keyword.objects.filter(name="Adventure").first()
        romance_keyword = Keyword.objects.filter(name="Romance").first()
        action_keyword = Keyword.objects.filter(name="Action").first()

        for i, manuscript_data in enumerate(sample_manuscripts):
            author = authors[i % len(authors)]

            manuscript, created = Manuscript.objects.get_or_create(
                title=manuscript_data["title"],
                author=author,
                defaults={
                    "description": manuscript_data["description"],
                    "plot_summary": manuscript_data["plot_summary"],
                    "status": manuscript_data["status"],
                    "budget": manuscript_data["budget"],
                    "beta_readers_needed": manuscript_data["beta_readers_needed"],
                    "nda_required": random.choice([True, False]),
                },
            )

            if created:
                self.stdout.write(f"Created manuscript: {manuscript.title}")

                # Add some keywords to manuscripts
                if adventure_keyword:
                    manuscript.keywords.add(adventure_keyword)
                if i % 2 == 0 and action_keyword:
                    manuscript.keywords.add(action_keyword)
                if "romance" in manuscript.title.lower() and romance_keyword:
                    manuscript.keywords.add(romance_keyword)

                # Add feedback questions to manuscripts
                questions = FeedbackQuestion.objects.all()[:5]
                manuscript.feedback_questions.set(questions)

        self.stdout.write(self.style.SUCCESS("Successfully created sample data!"))
        self.stdout.write(self.style.SUCCESS("Sample login credentials:"))
        self.stdout.write("Authors: author1/author2/author3 (password: password123)")
        self.stdout.write(
            "Beta Readers: reader1/reader2/reader3/reader4 (password: password123)"
        )
        self.stdout.write(
            "Admin: admin (password: set using manage.py changepassword admin)"
        )
