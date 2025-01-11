from django import forms
from .models import Manuscript
from django.utils.translation import gettext_lazy as _


class ManuscriptSubmissionForm(forms.ModelForm):
    class Meta:
        model = Manuscript
        fields = [
            "title",
            "file_path",
            "keywords",
            "budget",
            "beta_readers_needed",
            "cover_art",
            "nda_required",
            "nda_file",
            "plot_summary",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"autocomplete": "off"}),
            "file_path": forms.TextInput(attrs={"autocomplete": "off"}),
            "keywords": forms.TextInput(attrs={"autocomplete": "off"}),
            "budget": forms.NumberInput(attrs={"autocomplete": "off"}),
            "beta_readers_needed": forms.NumberInput(attrs={"autocomplete": "off"}),
            "cover_art": forms.ClearableFileInput(attrs={"autocomplete": "off"}),
            "nda_required": forms.CheckboxInput(attrs={"autocomplete": "off"}),
            "nda_file": forms.ClearableFileInput(attrs={"autocomplete": "off"}),
            "plot_summary": forms.Textarea(attrs={"autocomplete": "off"}),
        }
        labels = {
            "title": _("Title"),
            "file_path": _("Manuscript File"),
            "keywords": _("Genre & Keywords"),
            "budget": _("Budget Per Reader"),
            "beta_readers_needed": _("Number of Beta Readers"),
            "cover_art": _("Cover Art (Optional)"),
            "nda_required": _("Require NDA"),
            "nda_field": _("NDA File (Optional)"),
            "plot_summary": _("Manuscript Plot Summary"),
        }


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={"autocomplete": "username"})
    )
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
