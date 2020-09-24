import json
import base64
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import Postagem

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
            return JsonResponse({'message': True, 'id': user.pk})
        else:
            return JsonResponse({'message': False})
        print("a4")
    return JsonResponse({'message': False})

def postar(request):
    print(request.body)
    
    json_data = json.loads(request.body.decode())

    print(json_data)
    
    image_b64 = json_data['url_imagem'] # This is your base64 string image
    fmt, imgstr = image_b64.split(';base64,')
    ext = fmt.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

    Postagem.objects.create(
        url_imagem=data,
        enunciado=json_data['enunciado'],
        titulo=json_data['titulo'],
        usuario=User.objects.get(pk=json_data['usuario'])
    )
    
    return JsonResponse({'message': 'Teste'}) 

