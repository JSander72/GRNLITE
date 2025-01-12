from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
import my_app
from .views import (
    UserProfileView,
    BetaReaderListCreateView,
    ProfileListCreateView,
    ProfileDetailView,
    FeedbackQuestionListCreateView,
    ManuscriptFeedbackPreferenceListCreateView,
    ResourceListCreateView,
    ManuscriptListCreateView,
    ManuscriptDetailView,
    UserViewSet,
    ProfileViewSet,
    ManuscriptViewSet,
    save_token,
    UserCreate,
    SignInView,
    SignUpView,
)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"manuscripts", ManuscriptViewSet, basename="manuscript")

app_name = "my_app"

urlpatterns = [
    path("", views.home, name="home"),
    # User URLs
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    # path("api/signup/", SignUpView.as_view(), name="signup"),
    # path("api/signin/", SignInView.as_view(), name="signin"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    # Admin URLs
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("author-dashboard/", views.author_dashboard, name="author_dashboard"),
    path("reader-dashboard/", views.reader_dashboard, name="reader_dashboard"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
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
            [path("", include("djoser.urls")), path("", include("djoser.urls.jwt"))]
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
    path("signup/", UserCreate.as_view(), name="user-create"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
