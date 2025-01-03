from rest_framework import serializers

# from my_app.models import CustomUser
from .models import (
    Profile,
    Manuscript,
    Keyword,
    FeedbackQuestion,
    FeedbackResponse,
    AuthorSettings,
    Resource,
    ResourceInteraction,
    Notification,
    BetaReaderApplication,
    ManuscriptFeedbackPreference,
    Feedback,
    CustomUser,
    BetaReader,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "profile_picture"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "role",
            "profile_img",
            "bio",
            "created_at",
            "updated_at",
        ]


class ManuscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuscript
        fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "name", "category"]


class FeedbackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackQuestion
        fields = ["id", "question_text", "is_active"]


class FeedbackResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackResponse
        fields = [
            "id",
            "manuscript",
            "reader",
            "question",
            "answer_text",
            "review_date",
        ]


class AuthorSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorSettings
        fields = [
            "id",
            "author",
            "feedback_preferences",
            "notification_preferences",
            "profile_visibility",
            "auto_submit_feedback",
            "created_at",
            "updated_at",
        ]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            "id",
            "creator",
            "title",
            "description",
            "file",
            "created_at",
            "updated_at",
        ]


class ResourceInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceInteraction
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class BetaReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetaReader
        fields = ["id", "user", "experience", "genres", "created_at", "updated_at"]


class BetaReaderApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetaReaderApplication
        fields = "__all__"


class ManuscriptFeedbackPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuscriptFeedbackPreference
        fields = ["id", "manuscript", "question"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
