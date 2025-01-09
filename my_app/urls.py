from django.urls import path, include
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
    ReaderDashboardView,
    ReaderDashboardTemplateView,
    AuthorDashboardTemplateView,
    OAuth2LoginView,
    find_beta_readers,
    beta_reader_list,
)
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.contrib import admin


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

app_name = "my_app"

urlpatterns = [
    path("", views.home, name="home"),
    # User URLs
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),  # Include the router URLs here
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/user/", include(router.urls)),
    # User URLs
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # Auth URLs
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("allauth.urls")),
    path("auth/social/", include("social_django.urls", namespace="social")),
    # Google OAuth2 URLs
    path("admin/", admin.site.urls),
    path("oauth/login/", OAuth2LoginView.as_view(), name="oauth-login"),
    path("", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),  # Include allauth URLs
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path("auth/profile/", UserProfileView.as_view(), name="user-profile"),
    # Profile URLs
    path("profiles/", ProfileListCreateView.as_view(), name="profile-list-create"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
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
    # Manuscript Feedback Preference URLs
    path(
        "manuscript-feedback-preferences/",
        ManuscriptFeedbackPreferenceListCreateView.as_view(),
        name="manuscript-feedback-preference-list-create",
    ),
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
    path(
        "feedback-questions/",
        FeedbackQuestionListCreateView.as_view(),
        name="feedback-question-list-create",
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
    path(
        "author-settings/",
        AuthorSettingsListCreateView.as_view(),
        name="author-settings-list-create",
    ),
    # Resource URLs
    path("resources/", ResourceListCreateView.as_view(), name="resource-list"),
    path("resources/<int:pk>/", ResourceDetailView.as_view(), name="resource-detail"),
    path("resources/", ResourceListCreateView.as_view(), name="resource-list-create"),
    path(
        "resource-interactions/<int:pk>/",
        ResourceInteractionDetailView.as_view(),
        name="resource-interaction-detail",
    ),
    path(
        "resource-interactions/",
        ResourceInteractionListCreateView.as_view(),
        name="resource-interaction-list-create",
    ),
    # Reader Dashboard URLs
    path(
        "reader-dashboard.html", ReaderDashboardView.as_view(), name="reader-dashboard"
    ),
    path(
        "reader-dashboard/template/",
        ReaderDashboardTemplateView.as_view(),
        name="reader-dashboard-template",
    ),
    path("author-dashboard/", views.author_dashboard, name="author-dashboard"),
    path(
        "author-dashboard/template/",
        AuthorDashboardTemplateView.as_view(),
        name="author-dashboard-template",
    ),
    path(
        "available-manuscripts/",
        views.available_manuscripts,
        name="available-manuscripts",
    ),
    path("reader-feedback/", views.reader_feedback, name="reader-feedback"),
    path("reader-profile/", views.reader_profile, name="reader-profile"),
    path(
        "beta-readers/",
        BetaReaderListCreateView.as_view(),
        name="beta-reader-list-create",
    ),
    path("beta-readers/", beta_reader_list, name="beta-reader-list"),
    path("find-beta-readers/", find_beta_readers, name="find-beta-readers"),
    path(
        "reader-resource-library/",
        views.reader_resource_library,
        name="reader-resource-library",
    ),
    path(
        "notifications/",
        NotificationListCreateView.as_view(),
        name="notification-list-create",
    ),
    path(
        "notifications/<int:pk>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    path(
        "beta-reader-applications/<int:pk>/",
        BetaReaderApplicationDetailView.as_view(),
        name="beta-reader-application-detail",
    ),
    # Static and Media Files
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
