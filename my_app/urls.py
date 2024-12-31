from django.urls import path, include, re_path
from . import views
from .views import (
    GoogleLoginView,
    UserProfileView,
    BetaReaderListCreateView,
    find_beta_readers,
    beta_reader_list,
    ProfileListCreateView,
    ProfileDetailView,
    KeywordListCreateView,
    KeywordDetailView,
    FeedbackQuestionListCreateView,
    FeedbackQuestionDetailView,
    ManuscriptFeedbackPreferenceListCreateView,
    ManuscriptFeedbackPreferenceDetailView,
    FeedbackResponseListCreateView,
    FeedbackResponseDetailView,
    AuthorSettingsListCreateView,
    AuthorSettingsDetailView,
    ResourceListCreateView,
    ResourceDetailView,
    ResourceInteractionListCreateView,
    ResourceInteractionDetailView,
    NotificationListCreateView,
    NotificationDetailView,
    BetaReaderApplicationDetailView,
    ManuscriptListCreateView,
    ManuscriptDetailView,
    UserListCreateView,
    UserDetailView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = "my_app"

urlpatterns = [
    path("", views.home, name="home"),
    # User URLs
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/social/", include("social_django.urls", namespace="social")),
    # Google OAuth2 URLs
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path("auth/profile/", UserProfileView.as_view(), name="user-profile"),
    # Profile URLs
    path("profiles/", ProfileListCreateView.as_view(), name="profile-list-create"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    # Manuscript URLs
    path(
        "manuscript-submission/",
        views.manuscript_submission,
        name="manuscript-submission",
    ),
    path(
        "manuscripts/",
        ManuscriptListCreateView.as_view(),
        name="manuscript-list-create",
    ),
    path(
        "manuscripts/<int:pk>/",
        ManuscriptDetailView.as_view(),
        name="manuscript-detail",
    ),
    # Keyword URLs
    path("keywords/", KeywordListCreateView.as_view(), name="keyword-list-create"),
    path("keywords/<int:pk>/", KeywordDetailView.as_view(), name="keyword-detail"),
    path("keyword/<int:pk>/", KeywordDetailView.as_view(), name="keyword-detail"),
    # Feedback Question URLs
    path(
        "feedback-questions/",
        FeedbackQuestionListCreateView.as_view(),
        name="feedback-question-list",
    ),
    path(
        "feedback-questions/<int:pk>/",
        FeedbackQuestionDetailView.as_view(),
        name="feedback-question-detail",
    ),
    path(
        "feedback/",
        FeedbackQuestionListCreateView.as_view(),
        name="feedback-list-create",
    ),
    path(
        "feedback/<int:pk>/",
        FeedbackQuestionDetailView.as_view(),
        name="feedback-detail",
    ),
    # Manuscript Feedback Preference URLs
    path(
        "manuscript-feedback-preferences/",
        ManuscriptFeedbackPreferenceListCreateView.as_view(),
        name="manuscript-feedback-preference-list",
    ),
    path(
        "manuscript-feedback-preferences/<int:pk>/",
        ManuscriptFeedbackPreferenceDetailView.as_view(),
        name="manuscript-feedback-preference-detail",
    ),
    # Feedback Response URLs
    path(
        "feedback-responses/",
        FeedbackResponseListCreateView.as_view(),
        name="feedback-response-list",
    ),
    path(
        "feedback-responses/<int:pk>/",
        FeedbackResponseDetailView.as_view(),
        name="feedback-response-detail",
    ),
    # Author Settings URLs
    path(
        "author-settings/",
        AuthorSettingsListCreateView.as_view(),
        name="author-settings-list",
    ),
    path(
        "author-settings/<int:pk>/",
        AuthorSettingsDetailView.as_view(),
        name="author-settings-detail",
    ),
    # Resource URLs
    path("resources/", ResourceListCreateView.as_view(), name="resource-list"),
    path(
        "resources/<int:pk>/",
        ResourceDetailView.as_view(),
        name="resource-detail",
    ),
    # Resource Interactions URLs
    path(
        "resource-interactions/",
        ResourceInteractionListCreateView.as_view(),
        name="resource-interaction-list",
    ),
    path(
        "resource-interactions/<int:pk>/",
        ResourceInteractionDetailView.as_view(),
        name="resource-interaction-detail",
    ),
    # Notification URLs
    path(
        "notifications/",
        NotificationListCreateView.as_view(),
        name="notification-list",
    ),
    path(
        "notifications/<int:pk>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    # Beta Reader Application URLs
    path(
        "beta-reader-list/", BetaReaderListCreateView.as_view(), name="beta-reader-list"
    ),
    path("find-beta-readers/", find_beta_readers, name="find-beta-readers"),
    path(
        "beta-reader-applications/<int:pk>/",
        BetaReaderApplicationDetailView.as_view(),
        name="beta-reader-application-detail",
    ),
    # Reader Dashboard URLs
    path("reader-dashboard/", views.reader_dashboard, name="reader-dashboard"),
    path(
        "available-manuscripts/",
        views.available_manuscripts,
        name="available-manuscripts",
    ),
    path("reader-feedback/", views.reader_feedback, name="reader-feedback"),
    path("reader-profile/", views.reader_profile, name="reader-profile"),
    path(
        "reader-resource-library/",
        views.reader_resource_library,
        name="reader-resource-library",
    ),
    path(
        "beta-reader-training/", views.beta_reader_training, name="beta-reader-training"
    ),
    path(
        "beta-reader-performance-metrics/",
        views.beta_reader_performance_metrics,
        name="beta-reader-performance-metrics",
    ),
    path("reader-payment-page/", views.reader_payment_page, name="reader-payment-page"),
    path("reader-settings/", views.reader_settings, name="reader-settings"),
    # Feedback and Author Dashboard URLs
    path("feedback/<int:manuscript_id>/", views.feedback_form, name="feedback-form"),
    path("feedback-success/", views.feedback_success, name="feedback-success"),
    path("author-dashboard/", views.author_dashboard, name="author-dashboard"),
    path("my-manuscripts/", views.my_manuscripts, name="my-manuscripts"),
    path("my-books/", views.my_books, name="my-books"),
    path("author-profile/", views.author_profile, name="author-profile"),
    path("feedback-summary/", views.feedback_summary, name="feedback-summary"),
    path("manuscript-submission/", views.create_manuscript, name="create-manuscript"),
    path("manuscript-success/", views.manuscript_success, name="manuscript-success"),
    path(
        "author-resource-library/",
        views.author_resource_library,
        name="author-resource-library",
    ),
    path(
        "author-community-groups/",
        views.author_community_groups,
        name="author-community-groups",
    ),
    path("author-payment-page/", views.author_payment_page, name="author-payment-page"),
    path("author-settings/", views.author_settings, name="author-settings"),
    path("beta-readers/", beta_reader_list, name="beta_reader_list"),
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "beta-reader-list/", BetaReaderListCreateView.as_view(), name="beta-reader-list"
    ),
    path("notifications/", NotificationListCreateView.as_view(), name="notifications"),
    path(
        "resource-interactions/",
        ResourceInteractionListCreateView.as_view(),
        name="resource-interactions",
    ),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path(
        "feedback-questions/",
        FeedbackQuestionListCreateView.as_view(),
        name="feedback-questions",
    ),
    path(
        "author-settings/",
        AuthorSettingsListCreateView.as_view(),
        name="author-settings",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
