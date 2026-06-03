from django.contrib import admin

from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name', 'description')
	prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'author', 'publish_date', 'is_published', 'distributors_only')
	list_filter = ('category', 'is_published', 'distributors_only', 'publish_date')
	search_fields = ('title', 'content', 'meta_title', 'meta_description')
	prepopulated_fields = {'slug': ('title',)}
