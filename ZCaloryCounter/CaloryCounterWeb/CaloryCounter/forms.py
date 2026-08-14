from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, CalorieEntry

class RegistrationForm(forms.Form):
    username=forms.CharField(max_length=150,widget=forms.TextInput(attrs={"class":"input","placeholder":"Choose a username"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"input","placeholder":"you@example.com"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"input","placeholder":"Create a password"}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"input","placeholder":"Repeat your password"}))

    def clean_username(self):
        v=self.cleaned_data["username"]
        if User.objects.filter(username=v).exists(): raise forms.ValidationError("Username already exists.")
        return v

    def clean(self):
        c=super().clean()
        if c.get("password")!=c.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return c

class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"input","placeholder":"Username"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"input","placeholder":"Password"}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["name","age","gender","height_cm","weight_kg","activity_level"]
        widgets={
            "name":forms.TextInput(attrs={"class":"input","placeholder":"Your full name"}),
            "age":forms.NumberInput(attrs={"class":"input","min":1,"placeholder":"Age"}),
            "gender":forms.Select(attrs={"class":"input"}),
            "height_cm":forms.NumberInput(attrs={"class":"input","step":"0.1","placeholder":"Height in cm"}),
            "weight_kg":forms.NumberInput(attrs={"class":"input","step":"0.1","placeholder":"Weight in kg"}),
            "activity_level":forms.Select(attrs={"class":"input"}),
        }

class CalorieEntryForm(forms.ModelForm):
    class Meta:
        model=CalorieEntry
        fields=["item_name","calories"]
        widgets={
            "item_name":forms.TextInput(attrs={"class":"input","placeholder":"e.g. Chicken rice"}),
            "calories":forms.NumberInput(attrs={"class":"input","min":0,"placeholder":"e.g. 450"}),
        }
