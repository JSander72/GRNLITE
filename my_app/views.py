import json
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import generics, permissions, viewsets, serializers
from django.contrib.auth import get_user_model, login, authenticate, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .forms import ManuscriptSubmissionForm, SignupForm
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import get_or_create_user
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserSerializer
from django.urls import path

from .models import (
    Manuscript,
    Feedback,
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
    # FeedbackSerializer,
    # BetaReaderSerializer,
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .database import save_user
from rest_framework.authtoken.models import Token
from django.apps import apps
from django.db import IntegrityError

Profile = apps.get_model("my_app", "Profile")
Manuscript = apps.get_model("my_app", "Manuscript")
BetaReader = apps.get_model("my_app", "BetaReader")


def some_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()


class BetaReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetaReader
        fields = ["id", "user", "experience", "genres", "created_at", "updated_at"]


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["name"] = user.username
        token["role"] = user.profile.role  # Assuming the role is stored in the profile

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Check if the user_type is provided in the request body
        user_type = request.data.get("user_type")
        if user_type:
            response.data[
                "user_type"
            ] = user_type  # Add user_type to the token response

        return response


class ReaderDashboardView(APIView):
    """
    Provides an aggregated view of data relevant to the reader.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch manuscripts available to the reader
        manuscripts = Manuscript.objects.all()
        manuscripts_data = ManuscriptSerializer(manuscripts, many=True).data

        # Fetch notifications for the reader
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications_data = NotificationSerializer(notifications, many=True).data

        # Aggregate data into a dashboard response
        data = {
            "manuscripts": manuscripts_data,
            "notifications": notifications_data,
        }
        return Response(data)


class AuthorDashboardView(APIView):
    """
    Provides an aggregated view of data relevant to the author.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch manuscripts available to the author
        manuscripts = Manuscript.objects.filter(author=request.user)
        manuscripts_data = ManuscriptSerializer(manuscripts, many=True).data

        # Fetch notifications for the author
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications_data = NotificationSerializer(notifications, many=True).data

        # Aggregate data into a dashboard response
        data = {
            "manuscripts": manuscripts_data,
            "notifications": notifications_data,
        }
        return Response(data)


class ReaderDashboardTemplateView(TemplateView):
    """
    Serves the reader dashboard as an HTML template.
    """

    template_name = "reader-dashboard.html"


class AuthorDashboardTemplateView(TemplateView):
    """
    Serves the author dashboard as an HTML template.
    """

    template_name = "author-dashboard.html"


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures users can only access their own user details.
        """
        return User.objects.filter(id=self.request.user.id)


class ManuscriptListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating manuscripts.
    """

    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates the created manuscript with the logged-in user.
        """
        serializer.save(author=self.request.user)


class ManuscriptDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific manuscript.
    """

    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures users can only access their own manuscripts.
        """
        return Manuscript.objects.filter(author=self.request.user)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific profile.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures that a user can only access their own profile or profiles they are allowed to view.
        """
        return Profile.objects.filter(user=self.request.user)


class ProfileListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating profiles.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates the created profile with the currently logged-in user.
        """
        serializer.save(user=self.request.user)


class AuthorSettingsListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating author settings.
    """

    queryset = AuthorSettings.objects.all()
    serializer_class = AuthorSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates the created settings with the logged-in user.
        """
        serializer.save(author=self.request.user)


class AuthorSettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific author settings object.
    """

    queryset = AuthorSettings.objects.all()
    serializer_class = AuthorSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures a user can only access their own author settings.
        """
        return AuthorSettings.objects.filter(author=self.request.user)


class BetaReaderListCreateView(generics.ListCreateAPIView):
    queryset = BetaReader.objects.all()
    serializer_class = BetaReaderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Optionally add the currently logged-in user to the BetaReader object
        serializer.save(user=self.request.user)


class ResourceInteractionListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating resource interactions.
    """

    queryset = ResourceInteraction.objects.all()
    serializer_class = ResourceInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates the created interaction with the logged-in user.
        """
        serializer.save(user=self.request.user)


class ResourceListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating resources.
    """

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates the created resource with the logged-in user.
        """
        serializer.save(creator=self.request.user)


class ResourceInteractionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific resource interaction.
    """

    queryset = ResourceInteraction.objects.all()
    serializer_class = ResourceInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures users can only access their own resource interactions.
        """
        return ResourceInteraction.objects.filter(user=self.request.user)


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific resource.
    """

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures a user can only access resources they have created.
        """
        return Resource.objects.filter(creator=self.request.user)


class NotificationListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating notifications.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates the created notification with the logged-in user.
        """
        serializer.save(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific notification.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures users can only access their own notifications.
        """
        return Notification.objects.filter(user=self.request.user)


class KeywordListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating keywords.
    """

    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the keyword instance.
        """
        serializer.save()


class KeywordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific keyword.
    """

    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]


class BetaReaderApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific beta reader application.
    """

    queryset = BetaReaderApplication.objects.all()
    serializer_class = BetaReaderApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures users can only access their own beta reader applications.
        """
        return BetaReaderApplication.objects.filter(user=self.request.user)


class FeedbackQuestionListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating feedback questions.
    """

    queryset = FeedbackQuestion.objects.all()
    serializer_class = FeedbackQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the feedback question instance.
        """
        serializer.save()


class FeedbackResponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific feedback response.
    """

    queryset = FeedbackResponse.objects.all()
    serializer_class = FeedbackResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures users can only access their own feedback responses.
        """
        return FeedbackResponse.objects.filter(reader=self.request.user)


class FeedbackQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific feedback question.
    """

    queryset = FeedbackQuestion.objects.all()
    serializer_class = FeedbackQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ManuscriptFeedbackPreferenceListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating manuscript feedback preferences.
    """

    queryset = ManuscriptFeedbackPreference.objects.all()
    serializer_class = ManuscriptFeedbackPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the manuscript feedback preference instance.
        """
        serializer.save()


class ManuscriptFeedbackPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific manuscript feedback preference.
    """

    queryset = ManuscriptFeedbackPreference.objects.all()
    serializer_class = ManuscriptFeedbackPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeedbackResponseListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating feedback responses.
    """

    queryset = FeedbackResponse.objects.all()
    serializer_class = FeedbackResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates the feedback response with the currently logged-in user.
        """
        serializer.save(reader=self.request.user)


class InvalidKeyError(Exception):
    pass


class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "user": serializer.data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "message": "User created successfully",
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SignInView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = MyTokenObtainPairSerializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ManuscriptViewSet(viewsets.ModelViewSet):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# Home View
def home(request):
    return render(request, "main.html")


from django.contrib.auth import login as auth_login


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_type = request.POST["user_type"]

        try:
            user = User.objects.create_user(username=username, password=password)
            user.profile.user_type = (
                user_type  # Assuming you have a profile model with user_type field
            )
            user.save()

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            jwt_token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            login(request, user)
            return redirect("my_app:home")  # Redirect to home or any other page
        except IntegrityError:
            return render(request, "signup.html", {"error": "Username already exists"})
    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_type = request.POST["user_type"]  # Get the user type from the form

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user_type == "author":
                return redirect("my_app:author_dashboard")
            else:
                return redirect("my_app:reader_dashboard")
        else:
            return render(request, "signin.html", {"error": "Invalid credentials"})
    return render(request, "signin.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("signin")


def signin(request):
    return render(request, "signin.html")


def login(request):
    return render(request, "signin.html")


def logout(request):
    return render(request, "logout.html")


# Reader Dashboard Views
def reader_dashboard(request):
    return render(request, "reader-dashboard.html")


def reader_dashboard(request):
    return render(request, "available-manuscripts.html")


def reader_feedback(request):
    return render(request, "reader-feedback.html")


def reader_profile(request):
    return render(request, "reader-profile.html")


def reader_resource_library(request):
    return render(request, "reader-resource-library.html")


# Author Dashboard Views
def author_dashboard(request):
    return render(request, "author-dashboard.html")


def author_dashboard(request):
    return render(request, "my-manuscripts.html")


def manuscript_submission(request):
    return render(request, "manuscript-submission.html")


def manuscript_success(request):
    return render(request, "manuscript-success.html")


def my_books(request):
    return render(request, "my-books.html")


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
    return render(request, "manuscript-submission2.html", {"form": form})


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
        return redirect("feedback-success")
    return render(request, "reader-feedback.html", {"manuscript": manuscript})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reader_dashboard(request):
    # Your view logic here
    return HttpResponse("Reader Dashboard Content", content_type="text/html")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def author_dashboard(request):
    # Your view logic here
    return HttpResponse("Author Dashboard Content", content_type="text/html")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def find_beta_readers(request):
    """
    Filters beta readers based on query parameters.
    Query parameters:
        - experience (string): Text to match in experience field.
        - genres (list of IDs): Genre IDs to filter by.
    """
    experience_query = request.GET.get("experience", "")
    genres_query = request.GET.getlist("genres")

    # Filter beta readers by experience and genres
    beta_readers = BetaReader.objects.all()

    if experience_query:
        beta_readers = beta_readers.filter(experience__icontains=experience_query)
    if genres_query:
        beta_readers = beta_readers.filter(genres__id__in=genres_query).distinct()

    serializer = BetaReaderSerializer(beta_readers, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def beta_reader_list(request):
    """
    Returns a list of all beta readers.
    """


def beta_reader_list(request):
    beta_readers = BetaReader.objects.all()
    serializer = BetaReaderSerializer(beta_readers, many=True)
    return Response(serializer.data)


# Error 404 View
def error_404_view(request, exception):
    return render(request, "404.html", status=404)


def error_404_view(request, _exception):
    # Your login logic here
    return render(request, "signin.html")


@csrf_exempt
def save_token(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = data.get("token")
        user_id = data.get("user_id")
        if not token or not user_id:
            return JsonResponse({"error": "Token and user_id are required"}, status=400)
        try:
            user = User.objects.get(id=user_id)
            Token.objects.create(token=token, user=user)
            return JsonResponse({"message": "Token saved successfully"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


handler404 = error_404_view
