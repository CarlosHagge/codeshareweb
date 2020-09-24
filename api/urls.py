from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from . import views
from . import models
from .permissions import IsStaffOrTargetUser
from .views import check_user

from rest_framework import serializers    

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64 
        import uuid

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            self.fail('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = self.get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension, )

        data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

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
    serializer_class = UserSerializer
    model = User

    def get(self, request, *args, **kwargs):
        # use this if username is in url kwargs
        username = self.kwargs.get('username')
        password = self.kwargs.get('password')

        print(self.kwargs)

        # use this if username is being sent as a query parameter
        username = self.request.query_params.get('username')

        try:
            user = User.objects.get(username=username) # retrieve the user using username
            if user.validate(password):
                return Response({'message':True})
        except User.DoesNotExist:
            return Response({'message':False}) # return false as user does not exist
        else:
            return Response({'message':False}) # Otherwise, return True



class PostagemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Postagem
        fields = ['id', 'data_hora_postagem', 'titulo', 'enunciado', 'url_imagem', 'n_likes', 'n_dislikes', 'comments', 'usuario', 'email']


class PostagemViewSet(viewsets.ModelViewSet):
    url_imagem = Base64ImageField(
        max_length=None, use_url=True,
    )

    queryset = models.Postagem.objects.all()
    serializer_class = PostagemSerializer


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comentario
        fields = ['id', 'data_hora_comentario', 'texto_comentario', 'postagem', 'usuario']


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = models.Comentario.objects.all()
    serializer_class = ComentarioSerializer


router = routers.DefaultRouter()
router.register(r'postagens', PostagemViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'accounts', UserView, 'list')


urlpatterns = [
    path('', include(router.urls)),
    path('usuario_login/',csrf_exempt(views.check_user)),
    path('postar/',csrf_exempt(views.postar))

]
