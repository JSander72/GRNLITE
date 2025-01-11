from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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
    ManuscriptViewSet,
    UserViewSet,
    ProfileViewSet,
    save_token,
)

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"manuscripts", ManuscriptViewSet, basename="manuscript")

app_name = "my_app"

urlpatterns = [
    path("", views.home, name="home"),
    # User URLs
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path(
        "auth/",
        include(
            [
                path("", include("djoser.urls")),
                path("", include("djoser.urls.jwt")),
                # Remove OAuth-related URLs
                # path("social/", include("social_django.urls", namespace="social_django")),
                # path("provider/login/", views.login_view, name="login"),
                # path("accounts/", include("allauth.urls")),
            ]
        ),
    ),
    path(
        "profiles/",
        include(
            [
                path("", ProfileListCreateView.as_view(), name="profile-list-create"),
                path("<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
                path("me/", UserProfileView.as_view(), name="user-profile"),
            ]
        ),
    ),
    path(
        "manuscript-feedback-preferences/",
        ManuscriptFeedbackPreferenceListCreateView.as_view(),
        name="manuscript-feedback-preference-list",
    ),
    path(
        "feedback-questions/",
        FeedbackQuestionListCreateView.as_view(),
        name="feedback-question-list",
    ),
    path("resources/", ResourceListCreateView.as_view(), name="resource-list"),
    path(
        "beta-readers/",
        BetaReaderListCreateView.as_view(),
        name="beta-reader-list",
    ),
    # Auth URLs
    path(
        "auth/",
        include(
            [
                path("", include("djoser.urls")),
                path("", include("djoser.urls.jwt")),
                # Remove OAuth-related URLs
                # path("social/", include("social_django.urls", namespace="social")),
                # path("provider/login/", views.login_view, name="login"),
                # path("accounts/", include("allauth.urls")),
            ]
        ),
    ),
    # Profile URLs
    path(
        "profiles/",
        include(
            [
                path("", ProfileListCreateView.as_view(), name="profile-list-create"),
                path("<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
                path("me/", UserProfileView.as_view(), name="user-profile"),
            ]
        ),
    ),
    # Manuscript URLs
    path(
        "manuscripts/",
        include(
            [
                path(
                    "",
                    ManuscriptListCreateView.as_view(),
                    name="manuscript-list-create",
                ),
                path(
                    "<int:pk>/",
                    ManuscriptDetailView.as_view(),
                    name="manuscript-detail",
                ),
            ]
        ),
    ),
    path("save_token/", save_token, name="save_token"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
