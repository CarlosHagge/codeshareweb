from django import forms
from django.forms import ModelForm, Form
from api import models

class PostForm(ModelForm):
    class Meta:
        model = models.Postagem
        fields = [
            'titulo',
            'enunciado',
            'url_imagem'
        ]

class ComentarioForm(ModelForm):
    class Meta:
        model = models.Comentario
        
        fields = [
            'texto_comentario',
        ]


class MaratonistaForm(ModelForm):
    class Meta:
        model = models.Maratonista
        
        fields = [
            'data_nascimento',
            'faculdade',
        ]

        widgets = {
            'data_nascimento': forms.TextInput(
                attrs={'type': 'date'}
            ),
        }