"""
Middleware to redirect unverified users to email verification page.
"""

from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.http import JsonResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailVerificationMiddleware:
    """
    Middleware that ensures users with unverified emails are redirected
    to the email verification page when trying to access protected areas.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # URLs that don't require email verification
        self.exempt_urls = [
            "/verify-email/",
            "/api/resend-verification/",
            "/api/verification-status/",
            "/signin/",
            "/signup/",
            "/api/signin/",
            "/api/signup/",
            "/logout/",
            "/admin/",
            "/static/",
            "/media/",
            "/",  # Home page
            "/api/token/",
            "/api/token/refresh/",
        ]

        # URL patterns that don't require email verification
        self.exempt_patterns = [
            "admin",
            "static",
            "media",
            "home",
            "signin",
            "signup",
            "verify_email",
            "resend_verification",
            "verification_status",
        ]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Check if the user needs email verification before accessing the view.
        """
        # Skip verification for exempt URLs
        if self.is_exempt_url(request.path):
            return None

        # Skip verification for exempt URL patterns
        if self.is_exempt_pattern(request):
            return None

        # Skip verification for unauthenticated users
        if not request.user.is_authenticated:
            return None

        # Skip verification if user is a superuser
        if request.user.is_superuser:
            return None

        # Check if user's email is verified
        if not getattr(request.user, "is_email_verified", False):
            # For API requests, return JSON response
            if request.content_type == "application/json" or request.path.startswith(
                "/api/"
            ):
                return JsonResponse(
                    {
                        "error": "Email verification required",
                        "message": "Please verify your email address to access this resource.",
                        "requires_verification": True,
                    },
                    status=403,
                )

            # For regular requests, redirect to verification page
            return redirect("my_app:verify_email")

        return None

    def is_exempt_url(self, path):
        """Check if the URL path is in the exempt list."""
        for exempt_url in self.exempt_urls:
            if path.startswith(exempt_url):
                return True
        return False

    def is_exempt_pattern(self, request):
        """Check if the URL pattern name is in the exempt list."""
        try:
            resolver_match = resolve(request.path)
            if resolver_match.url_name in self.exempt_patterns:
                return True
            if (
                resolver_match.namespace
                and resolver_match.namespace in self.exempt_patterns
            ):
                return True
        except Exception:
            # If we can't resolve the URL, err on the side of caution
            pass
        return False
