from django.urls import path
from . import views

urlpatterns = [
    path("register", views._register_user),
    path("loginStatus", views._login_status),
    path("login", views._login_user),
    path("logout", views._logout_user),
]

