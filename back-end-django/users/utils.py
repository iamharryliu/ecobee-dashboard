from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json


def register_user(request):
    data = json.loads(request.body)
    username = data["username"]
    email = data["email"]
    password = data["password"]
    user = User.objects.create_user(username, email, password)
    user.save()


def get_login_status(request):
    return request.user.is_authenticated


def login_user(request):
    data = json.loads(request.body)
    email = data["email"]
    username = User.objects.get(email=email).username
    password = data["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return True


def logout_user(request):
    logout(request)

