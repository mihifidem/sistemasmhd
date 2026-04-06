from django import forms
from django.contrib import admin

from .models import Product, Resource


class ProductAdminForm(forms.ModelForm):
    content = forms.CharField(
        label='Contenido detallado (HTML)',
        widget=forms.Textarea(attrs={
            'rows': 30,
            'style': 'font-family: monospace; font-size: 13px; width: 100%;',
        }),
        required=False,
    )

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'category', 'distributor_price', 'public_price', 'units_per_box', 'stock', 'active')
    list_filter = ('active', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'slug', 'category', 'description', 'active'),
        }),
        ('Precios y stock', {
            'fields': ('distributor_price', 'public_price', 'units_per_box', 'stock'),
        }),
        ('Contenido de la página de detalle', {
            'description': 'Escribe HTML directamente. Se renderizará en la página pública del producto.',
            'fields': ('content',),
            'classes': ('wide',),
        }),
        ('Tarifas de distribución', {
            'description': 'Precio neto por unidad para cada tarifa. Si el precio de una tarifa es 0, se aplica el precio distribuidor por defecto.',
            'fields': ('tier1_price', 'tier2_price', 'tier3_price', 'tier4_price'),
        }),
    )


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display  = ('title', 'resource_type', 'product', 'is_public', 'active', 'order')
    list_filter   = ('resource_type', 'is_public', 'active', 'product')
    search_fields = ('title', 'description')
    list_editable = ('is_public', 'active', 'order')
    fieldsets = (
        ('Información', {
            'fields': ('title', 'description', 'resource_type', 'product', 'is_public', 'active', 'order'),
        }),
        ('Archivo o enlace', {
            'description': 'Sube un archivo O indica una URL externa. Si hay archivo, tiene preferencia.',
            'fields': ('file', 'url', 'thumbnail'),
        }),
    )
