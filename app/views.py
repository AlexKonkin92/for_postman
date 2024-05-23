from django.http import JsonResponse
from .user6 import reset_password
import logging
import threading 
from sendmail_project.ipa_api import bootstrap_ipa_api

def reset_password_view(request):

    if request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email parameter is missing.'}, status=400)
        
        #success, message = reset_password()
        success = True
        
        logging.warning("Test")
        logging.warning(threading.current_thread())
        IPA_API = bootstrap_ipa_api()
        
        try:
            message = IPA_API.Command.user_show('newuser', all=True)['result']
            return JsonResponse({'status': 'success', 'message': message})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        # if success:
        #     return JsonResponse({'status': 'success', 'message': message})
        # else:
        #     return JsonResponse({'status': 'error', 'message': message}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)