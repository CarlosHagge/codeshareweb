from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response

from . import views
from . import models
from .permissions import IsStaffOrTargetUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
 
    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),
    
    def get_queryset(self):
        return User.objects.all()

class UserExistsView(viewsets.ModelViewSet):
    model = User

    def get(self, request, *args, **kwargs):
        # use this if username is in url kwargs
        username = self.kwargs.get('username')
        password = self.kwargs.get('password')

        # use this if username is being sent as a query parameter
        username = self.request.query_params.get('username')

        try:
            user = User.objects.get(username=username) # retrieve the user using username
            if user.validate(password):
                return Response(data={'message':True})
        except User.DoesNotExist:
            return Response(data={'message':False}) # return false as user does not exist
        else:
            return Response(data={'message':False}) # Otherwise, return True

class PostagemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Postagem
        fields = ['id', 'data_hora_postagem', 'titulo', 'enunciado', 'url_imagem', 'n_likes', 'n_dislikes', 'comments', 'email']


class PostagemViewSet(viewsets.ModelViewSet):
    queryset = models.Postagem.objects.all()
    serializer_class = PostagemSerializer


class ComentarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Comentario
        fields = ['id', 'data_hora_comentario', 'texto_comentario', 'postagem']


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = models.Comentario.objects.all()
    serializer_class = ComentarioSerializer


router = routers.DefaultRouter()
router.register(r'postagens', PostagemViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'accounts', UserView, 'list')
router.register(r'usuario_login', UserExistsView, basename='User')


urlpatterns = [
    path('', include(router.urls))
]
