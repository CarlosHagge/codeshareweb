from django.http import JsonResponse
from django.contrib.auth.models import User
import json

def check_user(request):
    print(request)
    if request.method=='POST':
        json_data=json.loads(request.POST.get(['data']))
        print('Json:', json_data)
        user = User.objects.get(username=json_data['username'])
        
        if user.validate_password(json_data['password']) is None:
            return JsonResponse({'message': True})
        else:
            return JsonResponse({'message': False})
    return JsonResponse({'message': False})

