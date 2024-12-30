from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .forms import ManuscriptSubmissionForm
from django.views.generic import ListView, CreateView
from django.http import JsonResponse
from .models import Manuscript, Feedback
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from social_django.utils import load_strategy
from social_core.backends.google import GoogleOAuth2
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from .models import (
    Profile,
    Keyword,
    FeedbackQuestion,
    FeedbackResponse,
    ManuscriptFeedbackPreference,
    AuthorSettings,
    Resource,
    ResourceInteraction,
    Notification,
    BetaReaderApplication,
    BetaReader,
)
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    ManuscriptSerializer,
    KeywordSerializer,
    FeedbackQuestionSerializer,
    FeedbackResponseSerializer,
    AuthorSettingsSerializer,
    ResourceSerializer,
    ResourceInteractionSerializer,
    NotificationSerializer,
    BetaReaderApplicationSerializer,
    ManuscriptFeedbackPreferenceSerializer,
)


# Home View
def home(request):
    try:
        return render(request, "main.html")
    except Exception as e:
        print(f"Error loading template 'main.html': {e}")
        return JsonResponse({"error": "Failed to load template."}, status=500)


def signup(request):
    try:
        return render(request, "signup.html")
    except Exception as e:
        print(f"Error loading template 'signup.html': {e}")
        return JsonResponse({"error": "Failed to load template."}, status=500)


def signin(request):
    try:
        return render(request, "signin.html")
    except Exception as e:
        print(f"Error loading template 'signin.html': {e}")
        return JsonResponse({"error": "Failed to load template."}, status=500)


def login(request):
    try:
        return render(request, "login.html")
    except Exception as e:
        print(f"Error loading template 'login.html': {e}")
        return JsonResponse({"error": "Failed to load template."}, status=500)


def logout(request):
    try:
        return render(request, "logout.html")
    except Exception as e:
        print(f"Error loading template 'logout.html': {e}")
        return JsonResponse({"error": "Failed to load template."}, status=500)


# Reader Dashboard Views
def reader_dashboard(request):
    return render(request, "reader-dashboard.html")


def available_manuscripts(request):
    return render(request, "Reader_Dashboard/available-manuscripts.html")


def reader_feedback(request):
    return render(request, "Reader_Dashboard/reader-feedback.html")


def reader_profile(request):
    return render(request, "Reader_Dashboard/reader-profile.html")


def reader_resource_library(request):
    return render(request, "Reader_Dashboard/reader-resource-library.html")


def beta_reader_training(request):
    return render(request, "Reader_Dashboard/beta-reader-training.html")


def beta_reader_performance_metrics(request):
    return render(request, "Reader_Dashboard/beta-reader-performance-metrics.html")


def reader_payment_page(request):
    return render(request, "Reader_Dashboard/reader-payment-page.html")


def reader_settings(request):
    return render(request, "Reader_Dashboard/reader-settings.html")


# Author Dashboard Views
def author_dashboard(request):
    return render(request, "author-dashboard.html")


def my_manuscripts(request):
    return render(request, "Author_Dashboard/my-manuscripts.html")


def get_manuscripts(request):
    manuscripts = Manuscript.objects.all().values("id", "title", "description", "cover")
    return JsonResponse(list(manuscripts), safe=False)


def find_beta_readers(request):
    return render(request, "Author_Dashboard/beta-reader-list.html")


def manuscript_submission(request):
    return render(request, "Author_Dashboard/manuscript-submission.html")


def manuscript_success(request):
    return render(request, "Author_Dashboard/manuscript-success.html")


def my_books(request):
    return render(request, "Author_Dashboard/my-books.html")


@login_required
def create_manuscript(request):
    if request.method == "POST":
        form = ManuscriptSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            manuscript = form.save(commit=False)
            manuscript.author = request.user
            manuscript.save()
            form.save_m2m()
            return redirect("manuscript-success")
    else:
        form = ManuscriptSubmissionForm()

    return render(
        request, "Author_Dashboard/manuscript-submission2.html", {"form": form}
    )


def feedback_form(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)

    if request.method == "POST":
        feedback_data = request.POST
        Feedback.objects.create(
            manuscript=manuscript,
            user=request.user,
            plot=feedback_data.get("plot"),
            characters=feedback_data.get("characters"),
            pacing=feedback_data.get("pacing"),
            worldbuilding=feedback_data.get("worldbuilding"),
            comments=feedback_data.get("comments"),
        )
        return redirect("feedback_success")

    return render(request, "reader_feedback.html", {"manuscript": manuscript})


@csrf_exempt
@login_required
def submit_feedback(request):
    if request.method == "POST":
        manuscript_id = request.POST.get("manuscript")
        manuscript = Manuscript.objects.get(id=manuscript_id)
        Feedback.objects.create(
            manuscript=manuscript,
            reader=request.user,
            plot=request.POST.get("plot"),
            characters=request.POST.get("characters"),
            pacing=request.POST.get("pacing"),
            worldbuilding=request.POST.get("worldbuilding"),
            comments=request.POST.get("comments"),
        )
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def feedback_success(request):
    return render(request, "feedback_success.html")


def feedback_summary(request):
    return render(request, "Author_Dashboard/feedback-summary.html")


def author_resource_library(request):
    return render(request, "Author_Dashboard/author-resource-library.html")


def author_community_groups(request):
    return render(request, "Author_Dashboard/author-community-groups.html")


def author_profile(request):
    return render(request, "Author_Dashboard/author-profile.html")


def author_payment_page(request):
    return render(request, "Author_Dashboard/author-payment-page.html")


def author_settings(request):
    return render(request, "Author_Dashboard/author-settings.html")


# Protected View
def protected_view(request):
    return Response({"message": "This is a protected view."})


# Google Login View
class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token not provided"}, status=400)

        try:
            strategy = load_strategy(request)
            backend = GoogleOAuth2(strategy=strategy)
            user_data = backend.user_data(token)
            user, created = User.objects.get_or_create(
                email=user_data["email"], defaults={"username": user_data["email"]}
            )
            refresh = RefreshToken.for_user(user)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)}
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)


# API Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ManuscriptListCreateView(generics.ListCreateAPIView):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer


class ManuscriptDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer


class FeedbackResponseListCreateView(generics.ListCreateAPIView):
    queryset = FeedbackResponse.objects.all()
    serializer_class = FeedbackResponseSerializer


class FeedbackResponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeedbackResponse.objects.all()
    serializer_class = FeedbackResponseSerializer


from django.template.loader import get_template

try:
    get_template("Author_Dashboard/beta-reader-list.html")
    print("Template exists and is accessible.")
except Exception as e:
    print(f"Error: {e}")

from django.urls import path


class UserProfileView(View):
    def get(self, request):
        return HttpResponse("User Profile")


urlpatterns = [
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
]

from django.views import View
from django.http import HttpResponse
