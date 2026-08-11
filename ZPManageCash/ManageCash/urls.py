from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("add-cash/", views.add_cash, name="add_cash"),
    path("add-expense/", views.add_expense, name="add_expense"),
    path("transactions/", views.transactions, name="transactions"),
    path("cash/<int:pk>/delete/", views.delete_cash, name="delete_cash"),
    path("expense/<int:pk>/delete/", views.delete_expense, name="delete_expense"),
]
