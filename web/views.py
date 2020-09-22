from django.shortcuts import render, redirect
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


from api import models

from .forms import PostForm, MaratonistaForm, ComentarioForm

# Create your views here.

def index(request):
    data_dict = {}
    data_dict['posts'] = models.Postagem.objects.all()
    return render(request, 'index.html', data_dict)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registrar.html', {'form': form})

def post(request, post_id):
    data_dict = {}
    post = models.Postagem.objects.get(pk=post_id)
    if (request.method == 'POST') and request.user.is_authenticated and post.aberto:
        form = ComentarioForm(request.POST)
        data_dict['form'] = form
        comentario = form.save(commit=False)
        comentario.usuario = request.user
        comentario.postagem = post
        # salvar no bd e Redirecionar para o novo post
        comentario.save()
        return redirect('/post/' + str(post_id) + '#comentario-' + str(comentario.pk))
    else:
        data_dict['form'] = ComentarioForm()


    comentarios = post.comentarios_postagem.all()
    data_dict['post'] = post
    data_dict['comentarios'] = comentarios
    return render(request, 'post.html', data_dict)

@login_required
def votar_post(request, post_id, voto):
    if (voto == 'like'):
        models.voto_post(request.user, post_id, True)

    if (voto == 'dislike'):
        models.voto_post(request.user, post_id, False)

    return redirect('/post/' + str(post_id))

@login_required
def postar(request):
    data_dict = {}
    if (request.method == 'POST'):
        form = PostForm(request.POST, request.FILES)
        data_dict['form'] = form
        if form.is_valid():
            post = form.save(commit=False)
            post.usuario = request.user
            # salvar no bd e guardar o id do novo post
            post.save()
            return redirect('/post/' + str(post.pk))
    else:
        data_dict['form'] = PostForm()

    return render(request, 'postar.html', data_dict)

@login_required
def perfil(request, perfil_id):
    data_dict = {}
    usuario_perfil = User.objects.get(pk=perfil_id)
    data_dict['perfil'] = usuario_perfil
    if (request.method == 'POST'):
        if hasattr(usuario_perfil, 'maratonista'):
            form = MaratonistaForm(request.POST, instance=usuario_perfil.maratonista)
            data_dict['form'] = form

            if form.is_valid():
                perfil = form.save()
                return redirect('/perfil/' + str(perfil.usuario.pk))

        else:
            form = MaratonistaForm(request.POST)
            data_dict['form'] = form

            if form.is_valid():
                perfil = form.save(commit=False)
                perfil.usuario = request.user
                perfil.save()
                return redirect('/perfil/' + str(perfil.usuario.pk))
    else:
        try:
            data_dict['form'] = MaratonistaForm(instance=usuario_perfil.maratonista)
        except User.maratonista.RelatedObjectDoesNotExist:
            data_dict['form'] = MaratonistaForm()
        
    return render(request, 'perfil.html', data_dict)

@login_required
def votar_comentario(request, comentario_id, voto, post_id):

    if (voto == 'like'):
        models.voto_comentario(request.user, comentario_id, True)

    if (voto == 'dislike'):
        models.voto_comentario(request.user, comentario_id, False)

    return redirect('/post/' + str(post_id) + '#comentario-' + str(comentario_id))