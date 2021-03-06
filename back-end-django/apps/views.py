from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import (
    check_api,
    authorize,
    create_app,
    update_app,
    delete_app,
    get_apps,
    get_user_thermostats,
    get_app_thermostats,
    get_thermostat,
    get_runtime_report,
    set_hvac_mode,
    resume,
    set_climate,
    set_temperature_hold,
    send_message,
)


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
    except Exception as e:
        print(e)
        print("Unsuccessfully created app.")
        success = False
    else:
        print("Successfully created app.")
        success = True
    return JsonResponse({"success": success})


@csrf_exempt
def _update(request):
    try:
        update_app(request)
    except:
        print("Unsuccessfully updated app.")
        success = False
    else:
        print("Successfully updated app.")
        success = True
    return JsonResponse({"success": success})


@csrf_exempt
def _delete(request, key):
    try:
        delete_app(key)
    except:
        print("Unsuccessfully deleted app.")
        success = False
    else:
        print("Successfully deleted app.")
        success = True
    return JsonResponse({"success": success})


@csrf_exempt
def _get_apps(request):
    apps = get_apps(request)
    return JsonResponse(apps, safe=False)


# Thermostats


@csrf_exempt
def _get_user_thermostats(request):
    thermostats = get_user_thermostats(request)
    return JsonResponse(thermostats, safe=False)


@csrf_exempt
def _get_app_thermostats(request, key):
    thermostats = get_app_thermostats(key)
    return JsonResponse(thermostats, safe=False)


@csrf_exempt
def _get_thermostat(request, identifier):
    thermostat = get_thermostat(request, identifier)
    success = True if thermostat else False
    return JsonResponse({"success": success, "thermostat": thermostat})


@csrf_exempt
def _get_runtime_report(request, key, identifier):
    runtimeReport = get_runtime_report(key, identifier)
    return JsonResponse(runtimeReport)


# # Thermostat Actions


@csrf_exempt
def _set_hvac_mode(request):
    return JsonResponse({"success": set_hvac_mode(request)})


@csrf_exempt
def _resume(request):
    return JsonResponse({"success": resume(request)})


@csrf_exempt
def _set_climate(request):
    return JsonResponse({"success": set_climate(request)})


@csrf_exempt
def _set_temperature_hold(request):
    return JsonResponse({"success": set_temperature_hold(request)})


@csrf_exempt
def _send_message(request):
    return JsonResponse({"success": send_message(request)})
