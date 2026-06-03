from django.conf import settings
from django.db import models
from django.urls import reverse


class BlogCategory(models.Model):
	name = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(max_length=140, unique=True)
	description = models.CharField(max_length=255, blank=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'Categoria del blog'
		verbose_name_plural = 'Categorias del blog'

	def __str__(self):
		return self.name


class BlogPost(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
	content = models.TextField()
	publish_date = models.DateTimeField()
	meta_title = models.CharField(max_length=255, blank=True)
	meta_description = models.CharField(max_length=320, blank=True)
	is_published = models.BooleanField(default=True)
	distributors_only = models.BooleanField(default=False, verbose_name='Solo distribuidores', help_text='Si está marcado, este post solo es visible para distribuidores aprobados.')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-publish_date']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail', args=[self.slug])
