from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import routers, serializers, viewsets

from . import views
from . import models
from .permissions import IsStaffOrTargetUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
 
    def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

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


urlpatterns = [
    path('', include(router.urls))
]
