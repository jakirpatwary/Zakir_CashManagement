from datetime import datetime, time
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm, LoginForm, ProfileForm, CalorieEntryForm
from .models import Profile, CalorieEntry

def get_profile(user):
    profile, _ = Profile.objects.get_or_create(
        user=user, defaults={"name":user.username,"age":25,"gender":"M","height_cm":170,"weight_kg":65}
    )
    return profile

def register_view(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form=RegistrationForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=User.objects.create_user(form.cleaned_data["username"],form.cleaned_data["email"],form.cleaned_data["password"])
        Profile.objects.create(user=user,name=user.username,age=25,gender="M",height_cm=170,weight_kg=65)
        login(request,user)
        messages.success(request,"Welcome! Complete your profile to personalize your calorie target.")
        return redirect("profile")
    return render(request,"register.html",{"form":form})

def login_view(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form=LoginForm(request,data=request.POST or None)
    if request.method=="POST" and form.is_valid():
        login(request,form.get_user()); return redirect("dashboard")
    return render(request,"login.html",{"form":form})

@login_required
def logout_view(request):
    logout(request); return redirect("login")

@login_required
def profile_view(request):
    profile=get_profile(request.user)
    form=ProfileForm(request.POST or None,instance=profile)
    if request.method=="POST" and form.is_valid():
        form.save(); messages.success(request,"Profile updated successfully."); return redirect("dashboard")
    return render(request,"profile.html",{"form":form})

@login_required
def dashboard_view(request):
    profile=get_profile(request.user)
    today=datetime.now().date()
    entries=CalorieEntry.objects.filter(
        user=request.user,consumed_at__range=(datetime.combine(today,time.min),datetime.combine(today,time.max))
    )
    consumed=sum(e.calories for e in entries)
    required=profile.daily_calories()
    return render(request,"dashboard.html",{
        "profile":profile,"required":round(required,2),"consumed":consumed,
        "remaining":round(required-consumed,2),"lose_calories":round(max(required-500,0),2),
        "gain_calories":round(required+500,2),"entries":entries,
    })

@login_required
def add_calorie_view(request):
    form=CalorieEntryForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        e=form.save(commit=False); e.user=request.user; e.save()
        messages.success(request,"Food added to today's log."); return redirect("dashboard")
    return render(request,"add_calorie.html",{"form":form})

@login_required
def delete_calorie_view(request,pk):
    e=get_object_or_404(CalorieEntry,pk=pk,user=request.user)
    if request.method=="POST": e.delete(); messages.success(request,"Food entry removed.")
    return redirect("dashboard")
