from django.http import JsonResponse
from django.contrib.auth.models import User
import json

def check_user(request):
    print(request.body)
    if request.method=='POST':
        print("a1")
        json_data = json.loads(request.body.decode()) 
        print("a2")
        # print('Json:', json_data)
        user = User.objects.get(username=json_data['username'])
        print("a3")
        
        if user.check_password(json_data['password']):
            return JsonResponse({'message': True})
        else:
            return JsonResponse({'message': False})
        print("a4")
    return JsonResponse({'message': False})

