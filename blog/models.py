from django.conf import settings
from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
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
