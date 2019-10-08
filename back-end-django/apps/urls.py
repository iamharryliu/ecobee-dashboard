from django.urls import path
from . import views

urlpatterns = [
    path("checkAPI", views._check_api),
    path("authorize/<str:key>", views._authorize),
    path("create", views._create),
    path("update", views._update),
    path("delete/<str:key>", views._delete),
    # path("get", views._apps),
]
