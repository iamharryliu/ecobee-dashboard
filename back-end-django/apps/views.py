from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import check_api, authorize, create_app


@csrf_exempt
def _check_api(request):
    if check_api():
        success = True
    else:
        success = False
    return JsonResponse({"success": success})

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


@csrf_exempt
def _create(request):
    try:
        create_app(request)
    except:
        print("Successfully created app.")
        success = False
    else:
        print("Unsuccessfully created app.")
        success = True
    return JsonResponse({"success": success})

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

