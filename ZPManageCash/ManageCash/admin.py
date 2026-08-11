from django.contrib import admin

from .models import AddCash, Expense


@admin.register(AddCash)
class AddCashAdmin(admin.ModelAdmin):
    list_display = ("user", "source", "amount", "datetime")
    list_filter = ("datetime", "source")
    search_fields = ("user__username", "source", "description")
    ordering = ("-datetime",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "description", "amount", "datetime")
    list_filter = ("datetime",)
    search_fields = ("user__username", "description")
    ordering = ("-datetime",)
