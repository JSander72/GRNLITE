from django import forms
from .models import Manuscript, CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


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


class SignUpForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        choices=[("author", "Author"), ("beta_reader", "Reader")], required=True
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "user_type"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.user_type = self.cleaned_data["user_type"]  # Ensure user_type is set
        if commit:
            user.save()
        return user


class SignInForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]
