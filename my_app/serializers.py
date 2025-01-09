from rest_framework import serializers
from django.contrib.auth import get_user_model

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

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)  # Add this line

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "profile",  # Add this line
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="get_role_display", read_only=True)

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
        fields = [
            "id",
            "author",
            "title",
            "description",
            "plot_summary",  # Corrected field name
            "cover",
            "status",
            "created_at",
            "updated_at",
        ]


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
        fields = ["id", "user", "resource", "interaction_type", "timestamp"]


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
        fields = ["id", "user", "application_status", "applied_at", "updated_at"]


class ManuscriptFeedbackPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuscriptFeedbackPreference
        fields = ["id", "manuscript", "question"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
