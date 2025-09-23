from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django import forms
from .models import Manuscript, Profile, BetaReaderApplication
from django.contrib.auth import get_user_model

User = get_user_model()


class EnhancedManuscriptSubmissionForm(forms.ModelForm):
    """Enhanced form for manuscript submission with better validation"""

    class Meta:
        model = Manuscript
        fields = [
            "title",
            "description",
            "file_path",
            "plot_summary",
            "budget",
            "beta_readers_needed",
            "nda_required",
            "keywords",
            "feedback_questions",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter manuscript title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your manuscript",
                }
            ),
            "plot_summary": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Provide a brief plot summary",
                }
            ),
            "budget": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "placeholder": "Budget for beta reading",
                }
            ),
            "beta_readers_needed": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 10,
                    "placeholder": "Number of beta readers needed",
                }
            ),
            "nda_required": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "keywords": forms.CheckboxSelectMultiple(),
            "feedback_questions": forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_budget(self):
        budget = self.cleaned_data.get("budget")
        if budget < 0:
            raise ValidationError("Budget cannot be negative.")
        if budget > 10000:
            raise ValidationError("Budget cannot exceed $10,000.")
        return budget

    def clean_beta_readers_needed(self):
        count = self.cleaned_data.get("beta_readers_needed")
        if count < 1:
            raise ValidationError("At least one beta reader is required.")
        if count > 10:
            raise ValidationError("Maximum 10 beta readers allowed.")
        return count


class EnhancedProfileForm(forms.ModelForm):
    """Enhanced profile form with better validation"""

    class Meta:
        model = Profile
        fields = ["bio", "profile_img"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Tell us about yourself...",
                }
            ),
            "profile_img": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
        }

    def clean_bio(self):
        bio = self.cleaned_data.get("bio")
        if bio and len(bio) < 20:
            raise ValidationError("Bio must be at least 20 characters long.")
        return bio


class BetaReaderApplicationForm(forms.ModelForm):
    """Form for beta reader applications"""

    class Meta:
        model = BetaReaderApplication
        fields = ["cover_letter", "attachment"]
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Why are you interested in this manuscript? What relevant experience do you have?",
                }
            ),
            "attachment": forms.FileInput(
                attrs={"class": "form-control", "accept": ".pdf,.doc,.docx"}
            ),
        }

    def clean_cover_letter(self):
        cover_letter = self.cleaned_data.get("cover_letter")
        if not cover_letter:
            raise ValidationError("Cover letter is required.")
        if len(cover_letter) < 50:
            raise ValidationError("Cover letter must be at least 50 characters long.")
        return cover_letter


class UserSearchForm(forms.Form):
    """Form for searching users/manuscripts"""

    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search manuscripts, authors, or keywords...",
            }
        ),
    )

    SEARCH_CHOICES = [
        ("all", "All"),
        ("manuscripts", "Manuscripts"),
        ("authors", "Authors"),
        ("beta_readers", "Beta Readers"),
    ]

    search_type = forms.ChoiceField(
        choices=SEARCH_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
