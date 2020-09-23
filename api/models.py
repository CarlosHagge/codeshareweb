import time
from django.db import models
from django.contrib.auth.models import User


class Maratonista(models.Model):
	usuario = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		related_name='maratonista'
	)
	data_nascimento = models.DateField(blank=True)
	faculdade = models.CharField(max_length=512, blank=True)

	'''
	A data de registro (data_registro) pode ser acessada por date_joined
	(https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User.date_joined)
	'''

def post_img_path(instance, filename):
	ext = filename.split('.')[-1] # extensao da imagem
	return 'fts/{0}.{1}'.format(time.time(), ext)

class Postagem(models.Model):
	data_hora_postagem = models.DateTimeField(auto_now_add=True)
	titulo = models.CharField(max_length=256)
	enunciado = models.TextField(max_length=2048)
	url_imagem = models.ImageField(upload_to=post_img_path)
	aberto = models.BooleanField(default=True)
	usuario = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		related_name='postagens'
	)
	
	@property
	def n_likes(self):
		return VotoPostagem.objects.filter(postagem=self, positivo=True).count()

	@property
	def n_dislikes(self):
		return VotoPostagem.objects.filter(postagem=self, positivo=False).count()
	
	@property
	def email(self):
		# returna nome de usuario
		return self.usuario.username

	@property
	def comments(self):
		tmp_list = []
		comentarios = Comentario.objects.filter(postagem=self)
		for c in comentarios:
			tmp_list.append({'nickname': c.usuario.username,
			'comment': c.texto_comentario,
			'n_likes': c.n_likes,
			'n_dislikes': c.n_dislikes})

		return tmp_list

	class Meta:
		ordering = ['-data_hora_postagem']


class Comentario(models.Model):
	data_hora_comentario = models.DateTimeField(auto_now_add=True)
	texto_comentario = models.TextField(max_length=2048)
	postagem = models.ForeignKey(
		Postagem,
		on_delete=models.PROTECT,
		related_name='comentarios_postagem'
	)
	usuario = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		related_name='comentarios_usuario'
	)

	@property
	def n_likes(self):
		return VotoComentario.objects.filter(comentario=self, positivo=True).count()

	@property
	def n_dislikes(self):
		return VotoComentario.objects.filter(comentario=self, positivo=False).count()

	class Meta:
		ordering = ['-data_hora_comentario']


class VotoPostagem(models.Model):
	usuario = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		related_name='votos_postagem'
	)
	postagem = models.ForeignKey(
		Postagem,
		on_delete=models.PROTECT,
		related_name='votos_postagem'
	)

	# positivo: marca se eh like (quando true)
	positivo = models.BooleanField()

	class Meta:
		unique_together = ('usuario', 'postagem',)


def voto_post(usuario, postagem_id, tipo):
		postagem = Postagem.objects.get(pk=postagem_id)
		q = VotoPostagem.objects.filter(usuario=usuario, postagem=postagem)
		if q.exists():
			# q eh uma lista com 1 elemento
			q.update(positivo=tipo)			
		else:
			tmp = VotoPostagem(
				usuario=usuario,
				postagem=postagem,
				positivo=tipo
			)
			tmp.save()


class VotoComentario(models.Model):
	usuario = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		related_name='votos_comentario'
	)
	comentario = models.ForeignKey(
		Comentario,
		on_delete=models.PROTECT,
		related_name='votos_comentario'
	)

	# positivo: marca se eh like (quando true)
	positivo = models.BooleanField()

	class Meta:
		unique_together = ('usuario', 'comentario',)


def voto_comentario(usuario, comentario_id, tipo):
		comentario = Comentario.objects.get(pk=comentario_id)
		q = VotoComentario.objects.filter(usuario=usuario, comentario=comentario)
		if q.exists():
			# q eh uma lista com 1 elemento
			q.update(positivo=tipo)			
		else:
			tmp = VotoComentario(
				usuario=usuario,
				comentario=comentario,
				positivo=tipo
			)
			tmp.save()
