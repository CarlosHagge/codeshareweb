from django.http import JsonResponse
from django.contrib.auth.models import User

def check_user(request):
    if request.method=='POST':
        json_data=json.loads(request.POST['data'])
        print('Json:', json_data)
        user = User.objects.get(username=json_data['username'])
        
        if user.validate_password(json_data['password']) is None:
            return JsonResponse({'message': True})
        else:
            return JsonResponse({'message': False})

