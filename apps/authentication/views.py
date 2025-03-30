from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import register_user, authenticate_user
import json


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"success": False, "message": "Email and password are required."}, status=400)

            result = register_user(email, password)
            return JsonResponse(result, status=201 if result["success"] else 400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"success": False, "message": "Email and password are required."}, status=400)

            result = authenticate_user(email, password)
            return JsonResponse(result, status=200 if result["success"] else 401)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)