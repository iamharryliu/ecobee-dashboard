from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register),
    path("getLoggedInStatus", views.register),
    path("login", views.register),
    path("logout", views.register),
]

