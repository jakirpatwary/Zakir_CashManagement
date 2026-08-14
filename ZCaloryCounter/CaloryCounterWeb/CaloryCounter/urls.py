from django.urls import path
from . import views
urlpatterns=[
    path("",views.dashboard_view,name="dashboard"),
    path("register/",views.register_view,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("profile/",views.profile_view,name="profile"),
    path("food/add/",views.add_calorie_view,name="add_calorie"),
    path("food/delete/<int:pk>/",views.delete_calorie_view,name="delete_calorie"),
]
