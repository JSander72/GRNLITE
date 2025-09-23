from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    Manuscript,
    Profile,
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
    BetaReader,
    Genre,
    FeedbackCategory,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "user_type",
        )
        write_only_fields = ("password",)

    def validate(self, value):
        if User.objects.filter(email=value["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            user_type=validated_data["user_type"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
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


# class BetaReaderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BetaReader
#         fields = ["id", "user", "experience", "genres", "created_at", "updated_at"]


class BetaReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetaReader
        fields = ["id", "user", "experience", "genres", "created_at", "updated_at"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]


class FeedbackCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackCategory
        fields = ["id", "name", "description", "is_active"]


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
