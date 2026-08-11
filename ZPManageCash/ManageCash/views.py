from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AddCashForm,
    ExpenseForm,
    LoginForm,
    ProfileForm,
    RegistrationForm,
)
from .models import AddCash, Expense


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        identifier = form.cleaned_data["username_or_email"].strip()
        password = form.cleaned_data["password"]

        username = identifier
        if "@" in identifier:
            user = User.objects.filter(email__iexact=identifier).first()
            if user:
                username = user.username

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect("dashboard")

        form.add_error(None, "Invalid username/email or password.")

    return render(request, "ManageCash/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect("login")

    return render(request, "ManageCash/register.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect("login")
    return redirect("dashboard")


@login_required
def dashboard(request):
    cash_total = (
        AddCash.objects.filter(user=request.user)
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )
    expense_total = (
        Expense.objects.filter(user=request.user)
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )
    balance = cash_total - expense_total

    recent_cash = AddCash.objects.filter(user=request.user)[:5]
    recent_expenses = Expense.objects.filter(user=request.user)[:5]

    cash_count = AddCash.objects.filter(user=request.user).count()
    expense_count = Expense.objects.filter(user=request.user).count()

    context = {
        "cash_total": cash_total,
        "expense_total": expense_total,
        "balance": balance,
        "recent_cash": recent_cash,
        "recent_expenses": recent_expenses,
        "cash_count": cash_count,
        "expense_count": expense_count,
    }
    return render(request, "ManageCash/dashboard.html", context)


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("profile")

    return render(request, "ManageCash/profile.html", {"form": form})


@login_required
def add_cash(request):
    initial = {"datetime": timezone.localtime().strftime("%Y-%m-%dT%H:%M")}
    form = AddCashForm(request.POST or None, initial=initial)

    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.save()
        messages.success(request, "Cash income added successfully.")
        return redirect("dashboard")

    return render(request, "ManageCash/transaction_form.html", {
        "form": form,
        "transaction_type": "Add Cash",
        "transaction_icon": "bi-arrow-down-left-circle",
        "transaction_help": "Record money received from salary, business, freelance work, or another source.",
    })


@login_required
def add_expense(request):
    initial = {"datetime": timezone.localtime().strftime("%Y-%m-%dT%H:%M")}
    form = ExpenseForm(request.POST or None, initial=initial)

    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.save()
        messages.success(request, "Expense recorded successfully.")
        return redirect("dashboard")

    return render(request, "ManageCash/transaction_form.html", {
        "form": form,
        "transaction_type": "Add Expense",
        "transaction_icon": "bi-arrow-up-right-circle",
        "transaction_help": "Record money spent on food, transport, rent, shopping, bills, or other expenses.",
    })


@login_required
def transactions(request):
    cash_entries = AddCash.objects.filter(user=request.user)
    expense_entries = Expense.objects.filter(user=request.user)

    cash_total = cash_entries.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    expense_total = expense_entries.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    rows = []
    for item in cash_entries:
        rows.append({
            "id": item.id,
            "kind": "cash",
            "label": item.source,
            "description": item.description,
            "amount": item.amount,
            "datetime": item.datetime,
        })

    for item in expense_entries:
        rows.append({
            "id": item.id,
            "kind": "expense",
            "label": item.description,
            "description": "",
            "amount": item.amount,
            "datetime": item.datetime,
        })

    rows.sort(key=lambda x: x["datetime"], reverse=True)

    return render(request, "ManageCash/transactions.html", {
        "rows": rows,
        "cash_total": cash_total,
        "expense_total": expense_total,
        "balance": cash_total - expense_total,
    })


@login_required
def delete_cash(request, pk):
    if request.method == "POST":
        entry = get_object_or_404(AddCash, pk=pk, user=request.user)
        entry.delete()
        messages.success(request, "Cash entry deleted.")
    return redirect("transactions")


@login_required
def delete_expense(request, pk):
    if request.method == "POST":
        entry = get_object_or_404(Expense, pk=pk, user=request.user)
        entry.delete()
        messages.success(request, "Expense deleted.")
    return redirect("transactions")
