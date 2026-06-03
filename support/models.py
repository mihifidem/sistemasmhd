from django.db import models


class FAQ(models.Model):
	class Category(models.TextChoices):
		INFORMACION  = 'informacion',      'Información General sobre MHD'
		MHD_AGUA    = 'mhd_agua',        'MHD Agua'
		MHD_GAS     = 'mhd_gas',         'MHD Gas'
		TECH_SERVICE = 'servicio_tecnico', 'Servicio Técnico'
		INSTALACION  = 'instalacion',     'Instalación'	
		MANTENIMIENTO = 'mantenimiento',   'Mantenimiento'


	question     = models.CharField(max_length=255)
	answer       = models.TextField()
	category     = models.CharField(max_length=30, choices=Category.choices, default=Category.INFORMACION)
	display_order = models.PositiveIntegerField(default=0)
	is_active    = models.BooleanField(default=True)

	class Meta:
		ordering = ['category', 'display_order', 'id']

	def __str__(self):
		return self.question
