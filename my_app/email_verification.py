"""
Email verification utilities for sending verification codes and validating them.
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now
from django.utils.html import strip_tags
from .models import EmailVerification, CustomUser
import logging

logger = logging.getLogger(__name__)


def send_verification_email(user, email=None):
    """
    Send a verification email to the user with a verification code.

    Args:
        user: CustomUser instance
        email: Optional email address (defaults to user.email)

    Returns:
        EmailVerification instance if successful, None if failed
    """
    email_address = email or user.email

    try:
        # Create a new verification record
        verification = EmailVerification.objects.create(user=user, email=email_address)

        # Prepare email context
        context = {
            "user": user,
            "verification_code": verification.verification_code,
            "expiry_minutes": getattr(
                settings, "EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES", 15
            ),
            "site_name": "Grn Lite",
        }

        # Render email templates
        html_content = render_to_string("emails/verification_email.html", context)
        text_content = render_to_string("emails/verification_email.txt", context)

        # Create and send email
        subject = "Verify your email address - Grn Lite"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email_address]

        email_message = EmailMultiAlternatives(
            subject=subject, body=text_content, from_email=from_email, to=to_email
        )
        email_message.attach_alternative(html_content, "text/html")

        # Send the email
        email_message.send()

        logger.info(
            f"Verification email sent to {email_address} for user {user.username}"
        )
        return verification

    except Exception as e:
        logger.error(f"Failed to send verification email to {email_address}: {str(e)}")
        return None


def verify_email_code(user, verification_code, email=None):
    """
    Verify the email verification code for a user.

    Args:
        user: CustomUser instance
        verification_code: The verification code to check
        email: Optional email address (defaults to user.email)

    Returns:
        dict with 'success' boolean and 'message' string
    """
    email_address = email or user.email

    try:
        # Get the most recent unused verification code for this user and email
        verification = EmailVerification.objects.filter(
            user=user,
            email=email_address,
            verification_code=verification_code,
            is_used=False,
        ).first()

        if not verification:
            return {
                "success": False,
                "message": "Invalid verification code. Please check your code and try again.",
            }

        if verification.is_expired():
            return {
                "success": False,
                "message": "Verification code has expired. Please request a new code.",
            }

        # Mark the verification as used
        verification.is_used = True
        verification.used_at = now()
        verification.save()

        # Update user's email verification status
        user.is_email_verified = True
        user.email_verified_at = now()
        user.is_active = True  # Activate the user account
        user.save()

        logger.info(f"Email verified successfully for user {user.username}")

        return {
            "success": True,
            "message": "Email verified successfully! You can now access your account.",
        }

    except Exception as e:
        logger.error(f"Error verifying email for user {user.username}: {str(e)}")
        return {
            "success": False,
            "message": "An error occurred during verification. Please try again.",
        }


def resend_verification_code(user, email=None):
    """
    Resend a verification code to the user.

    Args:
        user: CustomUser instance
        email: Optional email address (defaults to user.email)

    Returns:
        dict with 'success' boolean and 'message' string
    """
    email_address = email or user.email

    # Check if user already has a valid (non-expired, unused) verification code
    existing_verification = (
        EmailVerification.objects.filter(user=user, email=email_address, is_used=False)
        .filter(expires_at__gt=now())
        .first()
    )

    if existing_verification:
        return {
            "success": False,
            "message": "A valid verification code has already been sent. Please check your email or wait for it to expire before requesting a new one.",
        }

    # Send new verification email
    verification = send_verification_email(user, email_address)

    if verification:
        return {
            "success": True,
            "message": "A new verification code has been sent to your email address.",
        }
    else:
        return {
            "success": False,
            "message": "Failed to send verification email. Please try again later.",
        }


def cleanup_expired_verifications():
    """
    Clean up expired verification codes.
    This should be run periodically as a maintenance task.
    """
    try:
        expired_count = EmailVerification.objects.filter(
            expires_at__lt=now(), is_used=False
        ).update(is_used=True)

        logger.info(f"Cleaned up {expired_count} expired verification codes")
        return expired_count

    except Exception as e:
        logger.error(f"Error cleaning up expired verifications: {str(e)}")
        return 0


def get_verification_status(user):
    """
    Get the current verification status for a user.

    Args:
        user: CustomUser instance

    Returns:
        dict with verification status information
    """
    if user.is_email_verified:
        return {
            "is_verified": True,
            "message": "Email is verified",
            "verified_at": user.email_verified_at,
        }

    # Check for pending verification
    pending_verification = (
        EmailVerification.objects.filter(user=user, email=user.email, is_used=False)
        .filter(expires_at__gt=now())
        .first()
    )

    if pending_verification:
        return {
            "is_verified": False,
            "has_pending": True,
            "message": "Verification code sent. Please check your email.",
            "expires_at": pending_verification.expires_at,
        }

    return {
        "is_verified": False,
        "has_pending": False,
        "message": "Email verification required",
    }
