from django.contrib import admin
from .models import Profile, CalorieEntry

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=("name","user","age","gender","height_cm","weight_kg","activity_level")
    search_fields=("name","user__username","user__email")

@admin.register(CalorieEntry)
class CalorieEntryAdmin(admin.ModelAdmin):
    list_display=("item_name","user","calories","consumed_at")
    list_filter=("consumed_at",)
    search_fields=("item_name","user__username")
