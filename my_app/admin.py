from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

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
    CustomUserGroup,
    CustomUserPermission,
    ExampleModel,
    UserToken,
)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [ProfileInline]
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("id",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


# Unregister the Profile model if it is already registered
try:
    admin.site.unregister(Profile)
except admin.sites.NotRegistered:
    pass


class ExampleModelAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at", "updated_at")
    list_filter = ("category", "is_active")
    search_fields = ("name", "category")


admin.site.register(ExampleModel, ExampleModelAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type")


admin.site.register(Profile, ProfileAdmin)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    def clean_user_type(self):
        user_type = self.cleaned_data.get("user_type")
        if not user_type:
            raise forms.ValidationError("User type is required.")
        return user_type


# Safely unregister and register CustomUser
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

admin.site.register(CustomUser, CustomUserAdmin)


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


class CustomUserGroupAdmin(admin.ModelAdmin):
    list_display = ("custom_user", "group")


class CustomUserPermissionAdmin(admin.ModelAdmin):
    list_display = ("custom_user", "permission")


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at")
    search_fields = ("user__username", "token")
    list_filter = ("created_at",)


admin.site.register(CustomUserGroup, CustomUserGroupAdmin)
admin.site.register(CustomUserPermission, CustomUserPermissionAdmin)
