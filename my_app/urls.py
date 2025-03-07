from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.views.generic import TemplateView
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
    protected_view,
    save_token,
    UserCreate,
    SignInView,
    SignUpView,
    reader_dashboard,
    author_dashboard,
    signup_page,
    register_user,
    ValidateTokenView,
)

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"manuscripts", ManuscriptViewSet, basename="manuscript")

app_name = "my_app"

urlpatterns = [
    # Home Page
    path("", views.home, name="home"),
    # Authentication URLs
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup_page/", views.signup_page, name="signup_page"),
    path("signin/", SignInView.as_view(), name="signin"),
    # path("signin/", TemplateView.as_view(template_name="signin.html"), name="signin"),
    path("signin/api/authenticate/", views.authenticate_user, name="signin_auth"),
    path("api/signup/", views.signup, name="signup"),
    path("api/signin/", views.signin, name="signin"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("api/protected/", protected_view, name="protected"),
    path("api/save_token/", save_token, name="save_token"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # Admin URLs
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("users/", include("djoser.urls")),
    path("jwt/", include("djoser.urls.jwt")),
    # Dashboard URLs
    path(
        "author-dashboard/",
        views.AuthorDashboardView.as_view(),
        name="author_dashboard",
    ),
    path(
        "reader-dashboard/",
        views.ReaderDashboardView.as_view(),
        name="reader_dashboard",
    ),
    path("reader-dashboard/", views.reader_dashboard, name="reader-dashboard"),
    path("author-dashboard/", views.author_dashboard, name="author-dashboard"),
    # Reader-Related URLs
    path("find-beta-readers/", views.find_beta_readers, name="find-beta-readers-html"),
    path("reader-feedback/", views.reader_feedback, name="reader-feedback-html"),
    path("reader-profile/", views.reader_profile, name="reader-profile-html"),
    path(
        "reader-payment-page/",
        views.reader_payment_page,
        name="reader-payment-page-html",
    ),
    path(
        "reader-resource-library/",
        views.reader_resource_library,
        name="reader-resource-library-html",
    ),
    path(
        "beta-reader-training/",
        views.beta_reader_training,
        name="beta-reader-training-html",
    ),
    path(
        "beta-reader-performance-metrics/",
        views.beta_reader_performance_metrics,
        name="beta-reader-performance-metrics-html",
    ),
    path("reader-settings/", views.reader_settings, name="reader-settings-html"),
    # Profile Management URLs
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
        "available-manuscripts/",
        views.available_manuscripts,
        name="available-manuscripts-html",
    ),
    # Manuscript Management URLs
    path("my-books/", views.my_books, name="my-books-html"),
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
    path(
        "manuscript-submission/",
        views.manuscript_submission,
        name="manuscript-submission-html",
    ),
    # Feedback Management URLs
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
    path("feedback-summary/", views.feedback_summary, name="feedback-summary-html"),
    # Resource Management URLs
    path("resources/", ResourceListCreateView.as_view(), name="resource-list"),
    path("beta-readers/", BetaReaderListCreateView.as_view(), name="beta-reader-list"),
    # API Router URLs
    path("api/", include(router.urls)),
    path("signup/", signup_page, name="signup_page"),
    path("register/", register_user, name="register_user"),
    path("protected/", protected_view, name="protected_view"),
    path("api/validate-token/", ValidateTokenView.as_view(), name="validate-token"),
    # Author Dashboard URLS
    path("beta-reader-list/", views.beta_reader_list, name="beta-reader-list-html"),
    path(
        "author-resource-library/",
        views.author_resource_library,
        name="author-resource-library-html",
    ),
    path(
        "author-community-groups/",
        views.author_community_groups,
        name="author-community-groups-html",
    ),
    path("author-profile/", views.author_profile, name="author-profile-html"),
    path(
        "author-payment-page/",
        views.author_payment_page,
        name="author-payment-page-html",
    ),
    path("author-settings/", views.author_settings, name="author-settings-html"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
