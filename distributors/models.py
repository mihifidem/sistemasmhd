from django.conf import settings
from django.db import models
from django.urls import reverse


class Distributor(models.Model):
	class CompanyType(models.TextChoices):
		INSTALLER = 'installer', 'Installer'
		SERVICE_CENTER = 'service_center', 'Service Center'
		DISTRIBUTOR = 'distributor', 'Distributor'

	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		APPROVED = 'approved', 'Approved'
		REJECTED = 'rejected', 'Rejected'

	class PriceTier(models.TextChoices):
		T1 = 'T1', 'Tarifa 1 — Básico'
		T2 = 'T2', 'Tarifa 2 — Plata'
		T3 = 'T3', 'Tarifa 3 — Oro'
		T4 = 'T4', 'Tarifa 4 — Platino'

	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='distributor_profile',
	)
	company_name = models.CharField(max_length=255)
	cif = models.CharField(max_length=30, unique=True)
	contact_person = models.CharField(max_length=255)
	email = models.EmailField()
	phone = models.CharField(max_length=30)
	address = models.CharField(max_length=255)
	province = models.CharField(max_length=120)
	city = models.CharField(max_length=120, blank=True)
	postal_code = models.CharField(max_length=20, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	company_type = models.CharField(max_length=20, choices=CompanyType.choices)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	services_offered = models.CharField(max_length=255, blank=True)
	bio = models.TextField(blank=True, verbose_name='Presentación / Bio', help_text='Descripción pública del distribuidor.')
	price_tier = models.CharField(
		max_length=2, choices=PriceTier.choices, default=PriceTier.T1,
		verbose_name='Tarifa de precios',
		help_text='Tarifa asignada por el administrador. Determina los precios aplicados a este distribuidor.',
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['company_name']

	def __str__(self):
		return self.company_name

	def get_absolute_url(self):
		return reverse('distributors:profile')

	@property
	def is_approved(self):
		return self.status == self.Status.APPROVED
