from django.http import JsonResponse
from .user6 import reset_password
import logging

def reset_password_view(request):

    if request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email parameter is missing.'}, status=400)
        
        #success, message = reset_password()
        success = True
        message = "test"
        logging.warning("Test")
        if success:
            return JsonResponse({'status': 'success', 'message': message})
        else:
            return JsonResponse({'status': 'error', 'message': message}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)