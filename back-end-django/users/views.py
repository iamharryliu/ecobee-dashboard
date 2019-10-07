from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import register_user, get_login_status, login_user, logout_user

# Create your views here.
@csrf_exempt
def _register_user(request):
    try:
        register_user(request)
    except:
        success = False
    else:
        success = True
    return JsonResponse({"success": success})


@csrf_exempt
def _login_status(request):
    status = get_login_status(request)
    return JsonResponse({"success": True, "status": status})


@csrf_exempt
def _login_user(request):
    success = True if login_user(request) else False
    return JsonResponse({"success": success})


@csrf_exempt
def _logout_user(request):
    logout_user(request)
    return JsonResponse({"success": True})
