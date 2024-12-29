from django.urls import path, include
from . import views
from .views import (
    GoogleLoginView,
    UserProfileView,
    BetaReaderListCreateView,
    find_beta_readers,
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
    path("users/", views.UserListCreateView.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/social/", include("social_django.urls", namespace="social")),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path("auth/profile/", UserProfileView.as_view(), name="user-profile"),
    # Profile URLs
    path("profiles/", views.ProfileListCreateView.as_view(), name="profile-list"),
    path(
        "profiles/<int:pk>/", views.ProfileDetailView.as_view(), name="profile-detail"
    ),
    # Manuscript URLs
    path(
        "manuscripts/", views.ManuscriptListCreateView.as_view(), name="manuscript-list"
    ),
    path(
        "manuscripts/<int:pk>/",
        views.ManuscriptDetailView.as_view(),
        name="manuscript-detail",
    ),
    path("manuscript-create/", views.create_manuscript, name="create-manuscript"),
    # Keyword URLs
    path("keywords/", views.KeywordListCreateView.as_view(), name="keyword-list"),
    path(
        "keywords/<int:pk>/", views.KeywordDetailView.as_view(), name="keyword-detail"
    ),
    # Feedback URLs
    path("feedback/<int:manuscript_id>/", views.feedback_form, name="feedback-form"),
    path("feedback-success/", views.feedback_success, name="feedback-success"),
    # Beta Reader URLs
    path("beta-readers/", BetaReaderListCreateView.as_view(), name="beta-reader-list"),
    path("find-beta-readers/", find_beta_readers, name="find-beta-readers"),
    # Dashboard URLs
    path("reader-dashboard/", views.reader_dashboard, name="reader-dashboard"),
    path("author-dashboard/", views.author_dashboard, name="author-dashboard"),
    path("feedback-summary/", views.feedback_summary, name="feedback-summary"),
    # Admin and Accounts
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
