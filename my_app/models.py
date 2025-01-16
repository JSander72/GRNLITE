from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()  # This will be CustomUser under the hood


class CustomUser(AbstractUser):
    genres = models.ManyToManyField("Genre", related_name="custom_users")
    groups = models.ManyToManyField(Group, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_set_permissions"
    )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=50,
        choices=[("reader", "Reader"), ("admin", "Admin")],
        default="reader",
    )
    name = models.CharField(max_length=255, default="Default Name")
    genre = models.CharField(max_length=255, default="Unknown")

    @staticmethod
    def update_existing_profiles():
        Profile.objects.filter(user_type="default_type").update(user_type="reader")

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


class Genre(models.Model):
    name = models.CharField(max_length=100, null=False, help_text="Name of the genre")
    description = models.TextField(
        null=True, blank=True, help_text="Description of the genre"
    )

    def __str__(self):
        return self.name


class Manuscript(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover = models.ImageField(upload_to="covers/")
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("in_review", "In Review"),
        ("completed", "Completed"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="manuscripts",
    )
    file_path = models.FileField(upload_to="uploads/manuscript/%Y/%m/%d/")
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="draft",
    )
    nda_required = models.BooleanField(default=False)
    keywords = models.ManyToManyField("Keyword", related_name="manuscripts", blank=True)
    budget = models.IntegerField(default=0)
    beta_readers_needed = models.IntegerField(default=0)
    cover_art = models.FileField(null=True, blank=True, upload_to="uploads/cover_art/")
    nda_file = models.FileField(null=True, blank=True, upload_to="uploads/nda/")
    plot_summary = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    manuscript = models.ForeignKey(
        Manuscript, on_delete=models.CASCADE, related_name="feedbacks"
    )
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )
    plot = models.TextField(null=True, blank=True)
    characters = models.TextField(null=True, blank=True)
    pacing = models.TextField(null=True, blank=True)
    worldbuilding = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)


class FeedbackQuestion(models.Model):
    question_text = models.TextField(help_text="Feedback question text")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text


class FeedbackResponse(models.Model):
    manuscript = models.ForeignKey(
        Manuscript, on_delete=models.CASCADE, related_name="feedback_responses"
    )
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedback_given",
    )
    question = models.ForeignKey(
        FeedbackQuestion, on_delete=models.CASCADE, related_name="responses"
    )
    answer_text = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.reader.username} for {self.manuscript.title}"


class Keyword(models.Model):
    name = models.CharField(max_length=100, help_text="Keyword for tagging")
    CATEGORY_CHOICES = [
        ("genre", "Genre"),
        ("theme", "Theme"),
    ]
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, help_text="Keyword category"
    )

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("read", "Read"), ("not_read", "Not Read")],
        default="not_read",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class BetaReaderApplication(models.Model):
    manuscript = models.ForeignKey(
        Manuscript, on_delete=models.CASCADE, related_name="applications"
    )
    beta_reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    reader_rating = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("applied", "Applied"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="applied",
    )
    application_date = models.DateTimeField(auto_now_add=True)


class ManuscriptFeedbackPreference(models.Model):
    # Define your fields here
    preference = models.CharField(
        max_length=10,
        choices=[
            ("applied", "Applied"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="applied",
    )
    application_date = models.DateTimeField(auto_now_add=True)


class AuthorSettings(models.Model):
    # Define your fields here
    setting_name = models.CharField(max_length=100)
    setting_value = models.CharField(max_length=100)


class ManuscriptFeedbackPreference(models.Model):
    preference = models.CharField(
        max_length=10,
        choices=[
            ("applied", "Applied"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="applied",
    )
    application_date = models.DateTimeField(auto_now_add=True)


class MyModel(models.Model):
    # Define your fields here
    field1 = models.CharField(max_length=100)


class ResourceInteraction(models.Model):
    # Define your fields here
    interaction_type = models.CharField(max_length=50)
    interaction_date = models.DateTimeField(auto_now_add=True)


class Resource(models.Model):
    resource_name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=50)


class AuthorSettings(models.Model):
    setting_name = models.CharField(max_length=100)
    setting_value = models.CharField(max_length=100)


class ManuscriptFeedbackPreference(models.Model):
    preference = models.CharField(
        max_length=10,
        choices=[
            ("applied", "Applied"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="applied",
    )
    application_date = models.DateTimeField(auto_now_add=True)
