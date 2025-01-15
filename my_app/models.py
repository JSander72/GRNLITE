from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now
from django.conf import settings


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
        Profile.objects.filter(role="default_type").update(role="reader")

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


class MyModel(models.Model):
    field1 = models.CharField(max_length=100)

    class Meta:
        db_table = "my_table_name"


class Keyword(models.Model):
    name = models.CharField(
        max_length=100, null=False, help_text="Keyword for tagging manuscripts"
    )
    CATEGORY_CHOICES = [
        ("genre", "Genre"),
        ("theme", "Theme"),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        null=False,
        help_text="Category of the keyword",
    )

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Feedback(models.Model):
    manuscript = models.ForeignKey(
        "Manuscript", on_delete=models.CASCADE, related_name="feedbacks"
    )
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    plot = models.TextField(null=True, blank=True)
    characters = models.TextField(null=True, blank=True)
    pacing = models.TextField(null=True, blank=True)
    worldbuilding = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)


class FeedbackQuestion(models.Model):
    question_text = models.TextField(help_text="The text of the feedback question")
    is_active = models.BooleanField(
        default=True, help_text="Is this question active and selectable?"
    )

    def __str__(self):
        return f"{self.question_text}"


class Manuscript(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The last time the manuscript was updated"
    )
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
        User,
        on_delete=models.CASCADE,
        related_name="manuscripts",
        help_text="The author of the manuscript",
    )
    file_path = models.FileField(upload_to="uploads/manuscript/%Y/%m/%d/")
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="draft",
        null=False,
        blank=True,
        help_text="Status of the manuscript",
    )
    nda_required = models.BooleanField(
        default=False,  # Default value to avoid NOT NULL constraint errors
        help_text="Indicates if an NDA is required for this manuscript",
    )
    keywords = models.ManyToManyField(
        Keyword,
        related_name="manuscripts",
        blank=True,
        help_text="Keywords associated with the manuscript",
    )
    budget = models.IntegerField(null=False, default=0)
    beta_readers_needed = models.IntegerField(null=False, default=0)
    cover_art = models.FileField(
        null=True, blank=True, upload_to="uploads/cover_art/%Y/%m/%d/"
    )
    nda_file = models.FileField(
        null=True, blank=True, upload_to="uploads/nda/%Y/%m/%d/"
    )
    plot_summary = models.TextField(max_length=1000, null=True)
    created_at = models.DateTimeField(default=now, help_text="Timestamp of creation")
    updated_at = models.DateTimeField(default=now, help_text="Timestamp of last update")

    def __str__(self):
        return self.title


class ManuscriptFeedbackPreference(models.Model):
    manuscript = models.ForeignKey(
        Manuscript, on_delete=models.CASCADE, related_name="feedback_preferences"
    )
    question = models.ForeignKey(
        FeedbackQuestion,
        on_delete=models.CASCADE,
        related_name="manuscript_preferences",
    )

    def __str__(self):
        return f"{self.manuscript.title} - {self.question.question_text}"


class FeedbackResponse(models.Model):
    manuscript = models.ForeignKey(
        Manuscript,
        on_delete=models.CASCADE,
        related_name="feedback_responses",
        help_text="The manuscript this feedback is for",
    )
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={
            "groups__name": "beta_reader"
        },  # Adjust group or role logic if necessary
        related_name="feedback_given",
        help_text="The beta reader providing the feedback",
    )
    question = models.ForeignKey(
        FeedbackQuestion,
        on_delete=models.CASCADE,
        help_text="The specific feedback question being answered",
    )
    answer_text = models.TextField(
        null=True, blank=True, help_text="The beta reader's answer to the question"
    )
    review_date = models.DateTimeField(
        auto_now_add=True, help_text="When the feedback was submitted"
    )

    def __str__(self):
        return f"Feedback by {self.reader.username} for {self.manuscript.title} - Question: {self.question.id}"


class AuthorSettings(models.Model):
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="settings",
        help_text="The author this settings configuration belongs to",
    )
    feedback_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Customizable preferences for the type of feedback the author wants",
    )
    notification_preferences = models.JSONField(
        default=dict, blank=True, help_text="Notification settings for the author"
    )
    profile_visibility = models.BooleanField(
        default=True, help_text="Whether the author's profile is public or private"
    )
    auto_submit_feedback = models.BooleanField(
        default=False,
        help_text="Automatically submit feedback requests when manuscripts are uploaded",
    )
    created_at = models.DateTimeField(
        default=now, help_text="Timestamp of when the settings were created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of when the settings were last updated"
    )

    def __str__(self):
        return f"Settings for {self.author.username}"


class Resource(models.Model):
    title = models.CharField(
        max_length=150, null=False, help_text="Title of the resource"
    )
    description = models.TextField(
        null=True, blank=True, help_text="Description of the resource"
    )
    file_path = models.FileField(
        upload_to="resources/",
        null=False,
        help_text="Path to the uploaded resource file",
    )
    category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Category of the resource (e.g., 'Templates', 'Guides')",
    )
    tags = models.TextField(
        null=True,
        blank=True,
        help_text="Comma-separated tags for search and categorization",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the resource was uploaded"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the resource was last updated"
    )

    def __str__(self):
        return self.title


class ResourceInteraction(models.Model):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="interactions"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resource_interactions",
        help_text="The user interacting with the resource",
    )
    interaction_type = models.CharField(
        max_length=50,
        choices=[("download", "Download"), ("favorite", "Favorite")],
        help_text="Type of user interaction",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp of the interaction"
    )

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.resource.title}"


class Notification(models.Model):
    STATUS_CHOICES = [
        ("read", "Read"),
        ("not_read", "Not Read"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="The user receiving the notification",
    )
    message = models.TextField(null=False, help_text="Message of the notification")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=False,
        help_text="Read status of the notification",
        default="not_read",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the notification was sent"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the notification was read"
    )
    is_read = models.BooleanField(default=False)


class BetaReaderApplication(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ("applied", "Applied"),  # Application submitted but not yet reviewed
        ("approved", "Approved"),  # Beta reader accepted by the author
        ("rejected", "Rejected"),  # Beta reader declined
    ]

    manuscript = models.ForeignKey(
        "Manuscript",
        on_delete=models.CASCADE,
        related_name="applications",
        help_text="The manuscript this application is for",
    )
    beta_reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={
            "groups__name": "beta_reader"
        },  # Or another method of filtering beta readers
        related_name="applications",
        help_text="The beta reader submitting the application",
    )
    reader_rating = models.IntegerField(
        null=True,
        blank=True,
        help_text="Optional rating given to the beta reader for their application",
    )
    attachment = models.FileField(
        upload_to="beta_reader_applications/",
        null=True,
        blank=True,
        help_text="Optional attachment for the beta reader's application",
    )
    status = models.CharField(
        max_length=10,
        choices=APPLICATION_STATUS_CHOICES,
        default="applied",
        help_text="Status of the application",
    )
    application_date = models.DateTimeField(
        auto_now_add=True, help_text="When the application was submitted"
    )
    review_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the application was reviewed by the author",
    )
    cover_letter = models.TextField(
        null=True,
        blank=True,
        help_text="Optional message from the beta reader to the author",
    )


class Genre(models.Model):
    name = models.CharField(max_length=100, null=False, help_text="Name of the genre")
    description = models.TextField(
        null=True, blank=True, help_text="Description of the genre"
    )

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    genres = models.ManyToManyField(Genre, related_name="custom_users")
    groups = models.ManyToManyField(Group, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_set_permissions"
    )


class BetaReader(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, related_name="beta_readers")
    experience = models.TextField(
        null=True, blank=True, help_text="Summary of the beta reader's experience"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the beta reader profile was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When the beta reader profile was last updated"
    )

    def __str__(self):
        return self.user.username


class ManuscriptKeywords(models.Model):
    manuscript = models.ForeignKey("Manuscript", on_delete=models.CASCADE)
    keyword = models.ForeignKey("Keyword", on_delete=models.CASCADE)
