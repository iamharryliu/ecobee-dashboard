from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import authorize

# Create your views here.
@csrf_exempt
def _authorize(request, key):
    try:
        pin, authorization_code = authorize(key)
    except:
        print("Unsuccessfuly authorized app.")
        success = False
        data = None
    else:
        print("Successfully authorized app.")
        success = True
        data = {"pin": pin, "authorization_code": authorization_code}
    return JsonResponse({"success": success, "data": data})


# @csrf_exempt
# def _create(request):
#     success = True
#     return JsonResponse({"success": success})


# @csrf_exempt
# def _update(request):
#     success = True
#     return JsonResponse({"success": success})


# @csrf_exempt
# def _delete(request):
#     success = True
#     return JsonResponse({"success": success})


# @csrf_exempt
# def _apps(request):
#     success = True
#     return JsonResponse({"success": success})

