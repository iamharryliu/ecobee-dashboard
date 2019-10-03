from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import register_user, get_login_status, login_user, logout_user

# Create your views here.
@csrf_exempt
def _authorize(request):
    success = True
    return JsonResponse({"success": success})


@csrf_exempt
def _create(request):
    success = True
    return JsonResponse({"success": success})


@csrf_exempt
def _update(request):
    success = True
    return JsonResponse({"success": success})


@csrf_exempt
def _delete(request):
    success = True
    return JsonResponse({"success": success})


@csrf_exempt
def _apps(request):
    success = True
    return JsonResponse({"success": success})

