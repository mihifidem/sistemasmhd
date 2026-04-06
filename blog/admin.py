from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'publish_date', 'is_published', 'distributors_only')
	list_filter = ('is_published', 'distributors_only', 'publish_date')
	search_fields = ('title', 'content', 'meta_title', 'meta_description')
	prepopulated_fields = {'slug': ('title',)}
