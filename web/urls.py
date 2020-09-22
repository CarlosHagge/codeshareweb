from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('postar/', views.postar),
    path('post/<int:post_id>', views.post),
    path('post/<int:post_id>/<str:voto>', views.votar_post),
    path('perfil/<int:perfil_id>', views.perfil),
    path('comentario/<int:comentario_id>/<str:voto>/<int:post_id>', views.votar_comentario),
    path('registrar/', views.signup)
]