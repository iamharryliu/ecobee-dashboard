import json
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({"test": "success"})


@csrf_exempt
def get_logged_in_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({"test": "success"})


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({"test": "success"})


@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({"test": "success"})
