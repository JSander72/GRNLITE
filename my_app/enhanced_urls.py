from django.urls import path, include
from .enhanced_views import (
    EnhancedManuscriptListView,
    EnhancedManuscriptDetailView,
    BetaReaderApplicationCreateView,
    UserDashboardView,
    NotificationListView,
    mark_notification_read,
    search_view,
    analytics_view,
)

# Enhanced API URLs
enhanced_api_patterns = [
    # Enhanced manuscript endpoints
    path(
        "manuscripts/",
        EnhancedManuscriptListView.as_view(),
        name="enhanced-manuscript-list",
    ),
    path(
        "manuscripts/<int:pk>/",
        EnhancedManuscriptDetailView.as_view(),
        name="enhanced-manuscript-detail",
    ),
    # Beta reader applications
    path(
        "applications/",
        BetaReaderApplicationCreateView.as_view(),
        name="beta-reader-application-create",
    ),
    # Dashboard and user data
    path("dashboard/", UserDashboardView.as_view(), name="user-dashboard"),
    path("analytics/", analytics_view, name="user-analytics"),
    # Notifications
    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path(
        "notifications/<int:notification_id>/read/",
        mark_notification_read,
        name="mark-notification-read",
    ),
    # Search
    path("search/", search_view, name="enhanced-search"),
]

# These should be added to the main urls.py as:
# path('api/v2/', include('my_app.enhanced_urls')),
