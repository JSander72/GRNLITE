from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import (
    Manuscript,
    Profile,
    BetaReader,
    BetaReaderApplication,
    FeedbackResponse,
    Notification,
)
from .serializers import (
    ManuscriptSerializer,
    ProfileSerializer,
    BetaReaderSerializer,
    BetaReaderApplicationSerializer,
    FeedbackResponseSerializer,
    NotificationSerializer,
)

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors to edit their own manuscripts."""

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the author of the manuscript
        return obj.author == request.user


class IsBetaReaderOrReadOnly(permissions.BasePermission):
    """Custom permission for beta reader related views."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name="beta_reader").exists()


class EnhancedManuscriptListView(generics.ListCreateAPIView):
    """Enhanced manuscript list view with filtering and search"""

    serializer_class = ManuscriptSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "keywords__name", "author"]
    search_fields = ["title", "description", "plot_summary"]
    ordering_fields = ["created_at", "title", "budget"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="author").exists():
            # Authors see their own manuscripts
            return Manuscript.objects.filter(author=user)
        elif user.groups.filter(name="beta_reader").exists():
            # Beta readers see available manuscripts for review
            return (
                Manuscript.objects.filter(status__in=["submitted", "in_review"])
                .annotate(application_count=Count("applications"))
                .exclude(applications__beta_reader=user)
            )
        else:
            # Regular users see published manuscripts
            return Manuscript.objects.filter(status="completed")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EnhancedManuscriptDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Enhanced manuscript detail view with permissions"""

    serializer_class = ManuscriptSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Manuscript.objects.all()


class BetaReaderApplicationCreateView(generics.CreateAPIView):
    """Create beta reader applications"""

    serializer_class = BetaReaderApplicationSerializer
    permission_classes = [IsAuthenticated, IsBetaReaderOrReadOnly]

    def perform_create(self, serializer):
        manuscript_id = self.request.data.get("manuscript")
        manuscript = Manuscript.objects.get(id=manuscript_id)

        # Check if user already applied
        if BetaReaderApplication.objects.filter(
            manuscript=manuscript, beta_reader=self.request.user
        ).exists():
            raise ValidationError("You have already applied to this manuscript.")

        serializer.save(beta_reader=self.request.user)


class UserDashboardView(APIView):
    """Enhanced dashboard view for different user types"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "user": {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_type": user.user_type,
            }
        }

        if user.groups.filter(name="author").exists():
            # Author dashboard data
            manuscripts = Manuscript.objects.filter(author=user)
            data.update(
                {
                    "manuscripts": ManuscriptSerializer(manuscripts, many=True).data,
                    "total_manuscripts": manuscripts.count(),
                    "draft_count": manuscripts.filter(status="draft").count(),
                    "submitted_count": manuscripts.filter(status="submitted").count(),
                    "in_review_count": manuscripts.filter(status="in_review").count(),
                    "completed_count": manuscripts.filter(status="completed").count(),
                    "recent_applications": BetaReaderApplicationSerializer(
                        BetaReaderApplication.objects.filter(
                            manuscript__author=user
                        ).order_by("-application_date")[:5],
                        many=True,
                    ).data,
                }
            )

        elif user.groups.filter(name="beta_reader").exists():
            # Beta reader dashboard data
            applications = BetaReaderApplication.objects.filter(beta_reader=user)
            available_manuscripts = Manuscript.objects.filter(
                status__in=["submitted", "in_review"]
            ).exclude(applications__beta_reader=user)[:10]

            data.update(
                {
                    "applications": BetaReaderApplicationSerializer(
                        applications, many=True
                    ).data,
                    "total_applications": applications.count(),
                    "approved_applications": applications.filter(
                        status="approved"
                    ).count(),
                    "pending_applications": applications.filter(
                        status="applied"
                    ).count(),
                    "available_manuscripts": ManuscriptSerializer(
                        available_manuscripts, many=True
                    ).data,
                    "completed_feedback": FeedbackResponse.objects.filter(
                        reader=user
                    ).count(),
                }
            )

        # Add notifications for all users
        notifications = Notification.objects.filter(
            user=user, status="not_read"
        ).order_by("-created_at")[:10]
        data["notifications"] = NotificationSerializer(notifications, many=True).data

        return Response(data)


class NotificationListView(generics.ListAPIView):
    """List user notifications"""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.status = "read"
        notification.save()
        return Response({"status": "success"})
    except Notification.DoesNotExist:
        return Response(
            {"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_view(request):
    """Enhanced search functionality"""
    query = request.GET.get("q", "")
    search_type = request.GET.get("type", "all")

    results = {}

    if not query:
        return Response({"error": "Search query is required"}, status=400)

    if search_type in ["all", "manuscripts"]:
        manuscripts = Manuscript.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(plot_summary__icontains=query)
            | Q(keywords__name__icontains=query)
        ).distinct()[:10]
        results["manuscripts"] = ManuscriptSerializer(manuscripts, many=True).data

    if search_type in ["all", "authors"]:
        authors = (
            User.objects.filter(groups__name="author")
            .filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(profile__bio__icontains=query)
            )
            .distinct()[:10]
        )
        results["authors"] = [
            {
                "id": author.id,
                "username": author.username,
                "name": f"{author.first_name} {author.last_name}",
                "bio": getattr(author.profile, "bio", "")
                if hasattr(author, "profile")
                else "",
            }
            for author in authors
        ]

    if search_type in ["all", "beta_readers"]:
        beta_readers = (
            User.objects.filter(groups__name="beta_reader")
            .filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(beta_reader_profile__experience__icontains=query)
            )
            .distinct()[:10]
        )
        results["beta_readers"] = [
            {
                "id": reader.id,
                "username": reader.username,
                "name": f"{reader.first_name} {reader.last_name}",
                "experience": getattr(reader.beta_reader_profile, "experience", "")
                if hasattr(reader, "beta_reader_profile")
                else "",
            }
            for reader in beta_readers
        ]

    return Response(results)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analytics_view(request):
    """Provide analytics data for the dashboard"""
    user = request.user

    if not user.groups.filter(name="author").exists():
        return Response({"error": "Only authors can access analytics"}, status=403)

    manuscripts = Manuscript.objects.filter(author=user)

    analytics = {
        "total_manuscripts": manuscripts.count(),
        "manuscripts_by_status": {
            "draft": manuscripts.filter(status="draft").count(),
            "submitted": manuscripts.filter(status="submitted").count(),
            "in_review": manuscripts.filter(status="in_review").count(),
            "completed": manuscripts.filter(status="completed").count(),
        },
        "total_applications": BetaReaderApplication.objects.filter(
            manuscript__author=user
        ).count(),
        "applications_by_status": {
            "applied": BetaReaderApplication.objects.filter(
                manuscript__author=user, status="applied"
            ).count(),
            "approved": BetaReaderApplication.objects.filter(
                manuscript__author=user, status="approved"
            ).count(),
            "rejected": BetaReaderApplication.objects.filter(
                manuscript__author=user, status="rejected"
            ).count(),
        },
        "total_feedback_received": FeedbackResponse.objects.filter(
            manuscript__author=user
        ).count(),
    }

    return Response(analytics)
