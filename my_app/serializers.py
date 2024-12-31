from rest_framework import serializers
from django.contrib.auth.models import User
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
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ManuscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuscript
        fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = "__all__"


class FeedbackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackQuestion
        fields = "__all__"


class FeedbackResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackResponse
        fields = "__all__"


class AuthorSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorSettings
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class ResourceInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceInteraction
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class BetaReaderApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetaReaderApplication
        fields = "__all__"


class ManuscriptFeedbackPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuscriptFeedbackPreference
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
