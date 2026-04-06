from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Resource(models.Model):
    class ResourceType(models.TextChoices):
        INFOGRAPHIC = 'infographic', 'Infografía'
        VIDEO       = 'video',       'Vídeo'
        AUDIO       = 'audio',       'Audio'
        PDF         = 'pdf',         'PDF'
        LINK        = 'link',        'Enlace externo'

    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices)
    product     = models.ForeignKey(
        'Product', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='resources',
        verbose_name='Producto relacionado',
    )
    # URL externa o path relativo al staticfiles
    url         = models.URLField(max_length=500, blank=True, help_text='URL externa (vídeo, enlace...)')
    file        = models.FileField(upload_to='resources/', blank=True, help_text='Archivo subido (PDF, imagen, audio...)')
    thumbnail   = models.ImageField(upload_to='resources/thumbs/', blank=True, help_text='Miniatura (opcional)')
    active      = models.BooleanField(default=True)
    is_public   = models.BooleanField(default=True, verbose_name='Público', help_text='Si está marcado, visible para todos. Si no, solo para distribuidores aprobados.')
    order       = models.PositiveSmallIntegerField(default=0, help_text='Orden de aparición')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return f'[{self.get_resource_type_display()}] {self.title}'

    @property
    def href(self):
        """Devuelve la URL de acceso al recurso (subido o externo)."""
        if self.file:
            return self.file.url
        return self.url


class Product(models.Model):
	class Category(models.TextChoices):
		WATER  = 'water',  'MHD Agua'
		GAS    = 'gas',    'MHD Gas'
		OTHER  = 'other',  'Otros productos'

	name = models.CharField(max_length=150, unique=True)
	slug = models.SlugField(max_length=160, unique=True, blank=True)
	category = models.CharField(
		max_length=20, choices=Category.choices, default=Category.OTHER,
		verbose_name='Categoría',
	)
	description = models.TextField()
	content = models.TextField(blank=True, default='', verbose_name='Contenido detallado (HTML)')
	distributor_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	tier1_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Precio Tarifa 1 (Básico)')
	tier2_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Precio Tarifa 2 (Plata)')
	tier3_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Precio Tarifa 3 (Oro)')
	tier4_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Precio Tarifa 4 (Platino)')
	public_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	units_per_box = models.PositiveIntegerField(default=1)
	stock = models.PositiveIntegerField(default=0)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def get_tier_price(self, tier):
		"""Returns the price for the given tier. Falls back to distributor_price if tier price is 0."""
		mapping = {
			'T1': self.tier1_price,
			'T2': self.tier2_price,
			'T3': self.tier3_price,
			'T4': self.tier4_price,
		}
		price = mapping.get(tier, Decimal('0.00'))
		return price if price else self.distributor_price

	def get_absolute_url(self):
		return reverse('products:detail', args=[self.slug])
