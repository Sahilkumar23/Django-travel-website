from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Journal, TripBooking


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "description", "location", "cover"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter journal title", "class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Write about your travel experience...",
                    "rows": 6,
                    "class": "form-control",
                }
            ),
            "location": forms.TextInput(
                attrs={"placeholder": "Enter travel location", "class": "form-control"}
            ),
            "cover": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }


class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("full_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        full_name = self.cleaned_data["full_name"].strip()
        parts = full_name.split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        if commit:
            user.save()
        return user


class TripPlanForm(forms.ModelForm):
    class Meta:
        model = TripBooking
        exclude = (
            "user",
            "status",
            "payment_method",
            "created_at",
            "updated_at",
        )
        widgets = {
            "depart_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "return_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "special_requests": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Any special requirements...",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        depart = cleaned_data.get("depart_date")
        ret = cleaned_data.get("return_date")
        if depart and ret and ret < depart:
            self.add_error("return_date", "Return date cannot be earlier than departure.")
        return cleaned_data
