from django.contrib import admin
from allauth.socialaccount.models import SocialAccount

# from my_app.models import CustomUser
from .models import (
    Manuscript,
    Profile,
    Keyword,
    FeedbackQuestion,
    ManuscriptFeedbackPreference,
    FeedbackResponse,
    AuthorSettings,
    Resource,
    BetaReaderApplication,
    ResourceInteraction,
    MyModel,
    CustomUser,
)


# admin.site.register(SocialAccount)


# admin.site.register(MyModel)
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ["field1"]


@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status")
    list_filter = ("status",)
    search_fields = ("title", "author__username")


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(FeedbackQuestion)
class FeedbackQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "is_active")
    list_filter = ("is_active",)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email"]


@admin.register(FeedbackResponse)
class FeedbackResponseAdmin(admin.ModelAdmin):
    list_display = ("manuscript", "reader", "question", "review_date")
    list_filter = ("review_date",)
    search_fields = ("manuscript__title", "reader__username")


@admin.register(AuthorSettings)
class AuthorSettingsAdmin(admin.ModelAdmin):
    list_display = ("author", "profile_visibility", "auto_submit_feedback")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("title",)


@admin.register(BetaReaderApplication)
class BetaReaderApplicationAdmin(admin.ModelAdmin):
    list_display = ("manuscript", "beta_reader", "status", "application_date")
    list_filter = ("status", "application_date")
    search_fields = ("manuscript__title", "beta_reader__username")
