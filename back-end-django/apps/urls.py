from django.urls import path
from . import views

urlpatterns = [
    path("authorize", views._authorize),
    path("create", views._create),
    path("update", views._update),
    path("delete", views._delete),
    path("get", views._apps),
]

