import os
import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grnlite.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_app.settings")
django.setup()

from django.test import TestCase
from my_app.models import (
    Profile,
    Manuscript,
    Genre,
    CustomUser,
    Keyword,
    Feedback,
    FeedbackQuestion,
    ManuscriptFeedbackPreference,
    FeedbackResponse,
    AuthorSettings,
    Resource,
    ResourceInteraction,
    Notification,
    BetaReaderApplication,
    BetaReader,
)
from django.contrib.auth.models import User, Group, Permission


class TestProfileModel(TestCase):
    def setUp(self):
        # Delete any existing "Test Manuscript" to avoid conflicts
        Manuscript.objects.filter(title="Test Manuscript").delete()

        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Create a profile
        self.profile = Profile.objects.create(
            user=self.user, profile_img="path/to/image.jpg"
        )

        # Create a genre
        self.genre = Genre.objects.create(name="Science Fiction")

        # Create a manuscript
        self.manuscript = Manuscript.objects.create(
            author=self.user,
            title="Initial Manuscript",
            file_path="/path/to/file",
            status="draft",
        )

    def test_profile_creation(self):
        profiles = Profile.objects.all()
        self.assertEqual(profiles.count(), 1)
        self.assertEqual(profiles[0].user.username, "testuser")

    def test_genre_creation(self):
        genres = Genre.objects.all()
        self.assertEqual(genres.count(), 1)
        self.assertEqual(genres[0].name, "Science Fiction")

    def test_manuscript_creation(self):
        # Create a new manuscript within the test
        Manuscript.objects.create(
            author=self.user,
            title="Test Manuscript",
            file_path="/path/to/file",
            status="draft",
        )
        manuscripts = Manuscript.objects.all()
        self.assertEqual(manuscripts.count(), 2)  # Change expected count to 2

    def test_manuscript_deletion(self):
        # Create a new manuscript specifically for this test
        manuscript_to_delete = Manuscript.objects.create(
            author=self.user,
            title="Manuscript to Delete",
            file_path="/path/to/file",
            status="draft",
        )

        manuscript_to_delete.delete()
        manuscripts = Manuscript.objects.all()

        # Expect 1 manuscript remaining: the one from setUp()
        self.assertEqual(manuscripts.count(), 1)  # Change expected count to 1

    def test_profile_update(self):
        self.profile.bio = "Updated bio"
        self.profile.save()
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, "Updated bio")

    def test_genre_update(self):
        self.genre.description = "Updated description"
        self.genre.save()
        updated_genre = Genre.objects.get(name="Science Fiction")
        self.assertEqual(updated_genre.description, "Updated description")

    def test_manuscript_update(self):
        self.manuscript.title = "Updated Manuscript"
        self.manuscript.save()
        updated_manuscript = Manuscript.objects.get(id=self.manuscript.id)
        self.assertEqual(updated_manuscript.title, "Updated Manuscript")

    def test_profile_deletion(self):
        self.profile.delete()
        profiles = Profile.objects.all()
        self.assertEqual(profiles.count(), 0)

    def test_genre_deletion(self):
        self.genre.delete()
        genres = Genre.objects.all()
        self.assertEqual(genres.count(), 0)


class TestModels(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.custom_user = CustomUser.objects.create(
            username="customuser", password="testpass"
        )

        # Create a profile
        self.profile = Profile.objects.create(
            user=self.user, profile_img="path/to/image.jpg"
        )

        # Create a genre
        self.genre = Genre.objects.create(name="Science Fiction")

        # Create a manuscript
        self.manuscript = Manuscript.objects.create(
            author=self.user,
            title="Initial Manuscript",
            file_path="/path/to/file",
            status="draft",
        )

        # Create a keyword
        self.keyword = Keyword.objects.create(name="Adventure", category="genre")

        # Create a feedback question
        self.feedback_question = FeedbackQuestion.objects.create(
            question_text="How was the plot?"
        )

        # Create a feedback response
        self.feedback_response = FeedbackResponse.objects.create(
            manuscript=self.manuscript,
            reader=self.user,
            question=self.feedback_question,
            answer_text="It was great!",
        )

        # Create author settings
        self.author_settings = AuthorSettings.objects.create(author=self.user)

        # Create a resource
        self.resource = Resource.objects.create(
            title="Resource Title",
            description="Resource Description",
            file_path="path/to/resource",
        )

        # Create a resource interaction
        self.resource_interaction = ResourceInteraction.objects.create(
            resource=self.resource, user=self.user, interaction_type="download"
        )

        # Create a notification
        self.notification = Notification.objects.create(
            user=self.user, message="This is a notification"
        )

        # Create a beta reader application
        self.beta_reader_application = BetaReaderApplication.objects.create(
            manuscript=self.manuscript, beta_reader=self.user
        )

        # Create a beta reader
        self.beta_reader = BetaReader.objects.create(user=self.user)

    def test_custom_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().username, "customuser")

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user.username, "testuser")

    def test_genre_creation(self):
        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(Genre.objects.first().name, "Science Fiction")

    def test_manuscript_creation(self):
        self.assertEqual(Manuscript.objects.count(), 1)
        self.assertEqual(Manuscript.objects.first().title, "Initial Manuscript")

    def test_keyword_creation(self):
        self.assertEqual(Keyword.objects.count(), 1)
        self.assertEqual(Keyword.objects.first().name, "Adventure")

    def test_feedback_question_creation(self):
        self.assertEqual(FeedbackQuestion.objects.count(), 1)
        self.assertEqual(
            FeedbackQuestion.objects.first().question_text, "How was the plot?"
        )

    def test_feedback_response_creation(self):
        self.assertEqual(FeedbackResponse.objects.count(), 1)
        self.assertEqual(FeedbackResponse.objects.first().answer_text, "It was great!")

    def test_author_settings_creation(self):
        self.assertEqual(AuthorSettings.objects.count(), 1)
        self.assertEqual(AuthorSettings.objects.first().author.username, "testuser")

    def test_resource_creation(self):
        self.assertEqual(Resource.objects.count(), 1)
        self.assertEqual(Resource.objects.first().title, "Resource Title")

    def test_resource_interaction_creation(self):
        self.assertEqual(ResourceInteraction.objects.count(), 1)
        self.assertEqual(
            ResourceInteraction.objects.first().interaction_type, "download"
        )

    def test_notification_creation(self):
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().message, "This is a notification")

    def test_beta_reader_application_creation(self):
        self.assertEqual(BetaReaderApplication.objects.count(), 1)
        self.assertEqual(
            BetaReaderApplication.objects.first().manuscript.title, "Initial Manuscript"
        )

    def test_beta_reader_creation(self):
        self.assertEqual(BetaReader.objects.count(), 1)
        self.assertEqual(BetaReader.objects.first().user.username, "testuser")

    def test_custom_user_update(self):
        self.custom_user.username = "updateduser"
        self.custom_user.save()
        self.assertEqual(CustomUser.objects.first().username, "updateduser")

    def test_profile_update(self):
        self.profile.bio = "Updated bio"
        self.profile.save()
        self.assertEqual(Profile.objects.first().bio, "Updated bio")

    def test_genre_update(self):
        self.genre.description = "Updated description"
        self.genre.save()
        self.assertEqual(Genre.objects.first().description, "Updated description")

    def test_manuscript_update(self):
        self.manuscript.title = "Updated Manuscript"
        self.manuscript.save()
        self.assertEqual(Manuscript.objects.first().title, "Updated Manuscript")

    def test_keyword_update(self):
        self.keyword.name = "Updated Keyword"
        self.keyword.save()
        self.assertEqual(Keyword.objects.first().name, "Updated Keyword")

    def test_feedback_question_update(self):
        self.feedback_question.question_text = "Updated Question"
        self.feedback_question.save()
        self.assertEqual(
            FeedbackQuestion.objects.first().question_text, "Updated Question"
        )

    def test_feedback_response_update(self):
        self.feedback_response.answer_text = "Updated Answer"
        self.feedback_response.save()
        self.assertEqual(FeedbackResponse.objects.first().answer_text, "Updated Answer")

    def test_author_settings_update(self):
        self.author_settings.profile_visibility = False
        self.author_settings.save()
        self.assertFalse(AuthorSettings.objects.first().profile_visibility)

    def test_resource_update(self):
        self.resource.title = "Updated Resource"
        self.resource.save()
        self.assertEqual(Resource.objects.first().title, "Updated Resource")

    def test_resource_interaction_update(self):
        self.resource_interaction.interaction_type = "favorite"
        self.resource_interaction.save()
        self.assertEqual(
            ResourceInteraction.objects.first().interaction_type, "favorite"
        )

    def test_notification_update(self):
        self.notification.status = "read"
        self.notification.save()
        self.assertEqual(Notification.objects.first().status, "read")

    def test_beta_reader_application_update(self):
        self.beta_reader_application.status = "approved"
        self.beta_reader_application.save()
        self.assertEqual(BetaReaderApplication.objects.first().status, "approved")

    def test_beta_reader_update(self):
        self.beta_reader.experience = "Updated Experience"
        self.beta_reader.save()
        self.assertEqual(BetaReader.objects.first().experience, "Updated Experience")

    def test_custom_user_deletion(self):
        self.custom_user.delete()
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_profile_deletion(self):
        self.profile.delete()
        self.assertEqual(Profile.objects.count(), 0)

    def test_genre_deletion(self):
        self.genre.delete()
        genres = Genre.objects.all()
        self.assertEqual(genres.count(), 0)

    def test_manuscript_deletion(self):
        self.manuscript.delete()
        self.assertEqual(Manuscript.objects.count(), 0)

    def test_keyword_deletion(self):
        self.keyword.delete()
        self.assertEqual(Keyword.objects.count(), 0)

    def test_feedback_question_deletion(self):
        self.feedback_question.delete()
        self.assertEqual(FeedbackQuestion.objects.count(), 0)

    def test_feedback_response_deletion(self):
        self.feedback_response.delete()
        self.assertEqual(FeedbackResponse.objects.count(), 0)

    def test_author_settings_deletion(self):
        self.author_settings.delete()
        self.assertEqual(AuthorSettings.objects.count(), 0)

    def test_resource_deletion(self):
        self.resource.delete()
        self.assertEqual(Resource.objects.count(), 0)

    def test_resource_interaction_deletion(self):
        self.resource_interaction.delete()
        self.assertEqual(ResourceInteraction.objects.count(), 0)

    def test_notification_deletion(self):
        self.notification.delete()
        self.assertEqual(Notification.objects.count(), 0)

    def test_beta_reader_application_deletion(self):
        self.beta_reader_application.delete()
        self.assertEqual(BetaReaderApplication.objects.count(), 0)

    def test_beta_reader_deletion(self):
        self.beta_reader.delete()
        self.assertEqual(BetaReader.objects.count(), 0)
