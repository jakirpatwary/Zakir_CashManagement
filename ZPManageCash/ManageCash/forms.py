from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import AddCash, Expense


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Username or Email",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Username or email",
            "autocomplete": "username",
        }),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Password",
            "autocomplete": "current-password",
        }),
    )


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Create a password",
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm password",
        })
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a username",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
            }),
        }

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm = cleaned.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Passwords do not match.")

        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as exc:
                self.add_error("password", exc)

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email address",
            }),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already used by another account.")
        return email


class AddCashForm(forms.ModelForm):
    class Meta:
        model = AddCash
        fields = ["source", "datetime", "amount", "description"]
        widgets = {
            "source": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Salary, Freelance, Business...",
            }),
            "datetime": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "min": "0.01",
                "step": "0.01",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Optional note",
                "rows": 4,
            }),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["description", "amount", "datetime"]
        widgets = {
            "description": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Food, Transport, Rent...",
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "min": "0.01",
                "step": "0.01",
            }),
            "datetime": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
        }
