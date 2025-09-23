from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from my_app.models import (
    Profile,
    Manuscript,
    AuthorSettings,
    FeedbackQuestion,
    FeedbackCategory,
    Keyword,
    Genre,
)
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Command(BaseCommand):
    help = "Load default data for the application"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Loading default data..."))

        # Create user groups
        author_group, created = Group.objects.get_or_create(name="author")
        beta_reader_group, created = Group.objects.get_or_create(name="beta_reader")

        if created:
            self.stdout.write(self.style.SUCCESS("Created user groups"))

        # Create default genres
        default_genres = [
            ("Fiction", "General fiction works"),
            ("Non-Fiction", "Non-fictional works"),
            ("Science Fiction", "Science fiction and speculative fiction"),
            ("Fantasy", "Fantasy and magical realism"),
            ("Romance", "Romance novels"),
            ("Mystery", "Mystery and detective stories"),
            ("Thriller", "Thriller and suspense"),
            ("Historical Fiction", "Historical fiction"),
            ("Literary Fiction", "Literary fiction"),
            ("Young Adult", "Young adult fiction"),
            ("Children's Books", "Children's literature"),
            ("Biography", "Biographical works"),
            ("Self-Help", "Self-help and personal development"),
        ]

        for genre_name, description in default_genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_name, defaults={"description": description}
            )
            if created:
                self.stdout.write(f"Created genre: {genre_name}")

        # Create default keywords
        default_keywords = [
            ("Adventure", "genre"),
            ("Romance", "genre"),
            ("Action", "theme"),
            ("Coming of Age", "theme"),
            ("Good vs Evil", "theme"),
            ("Love Triangle", "theme"),
            ("Magic System", "theme"),
            ("Political Intrigue", "theme"),
        ]

        for keyword_name, category in default_keywords:
            keyword, created = Keyword.objects.get_or_create(
                name=keyword_name, category=category
            )
            if created:
                self.stdout.write(f"Created keyword: {keyword_name} ({category})")

        # Create default feedback categories
        default_categories = [
            ("Plot", "Overall story structure and narrative flow"),
            ("Characters", "Character development and believability"),
            ("Dialogue", "Conversation quality and authenticity"),
            ("Pacing", "Story rhythm and timing"),
            ("World Building", "Setting and environment development"),
            ("Writing Style", "Prose quality and voice"),
            ("Grammar/Editing", "Technical writing aspects"),
        ]

        for cat_name, description in default_categories:
            category, created = FeedbackCategory.objects.get_or_create(
                name=cat_name, defaults={"description": description}
            )
            if created:
                self.stdout.write(f"Created feedback category: {cat_name}")

        # Create default feedback questions
        default_questions = [
            "What did you think of the overall plot structure?",
            "Were the characters believable and well-developed?",
            "How was the pacing throughout the story?",
            "Did the dialogue feel natural and engaging?",
            "What aspects of the world-building stood out to you?",
            "Were there any plot holes or inconsistencies you noticed?",
            "What was your favorite part of the manuscript?",
            "What areas need the most improvement?",
            "Would you recommend this book to others?",
            "How would you rate this manuscript overall (1-10)?",
        ]

        for question_text in default_questions:
            question, created = FeedbackQuestion.objects.get_or_create(
                question_text=question_text
            )
            if created:
                self.stdout.write(f"Created feedback question: {question_text[:50]}...")

        self.stdout.write(self.style.SUCCESS("Successfully loaded default data!"))
