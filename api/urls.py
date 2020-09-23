from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from . import views
from . import models

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


urlpatterns = [
    path('', include(router.urls))
]
