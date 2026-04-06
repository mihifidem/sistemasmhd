from decimal import Decimal

from django.db import models

from orders.models import Order


class Invoice(models.Model):
	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		PAID = 'paid', 'Paid'

	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='invoices')
	invoice_number = models.CharField(max_length=50, unique=True)
	issue_date = models.DateField()
	due_date = models.DateField()
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	payment_method = models.CharField(max_length=50, default='Bank transfer')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-issue_date']
		constraints = [
			models.UniqueConstraint(fields=['order'], name='unique_invoice_per_order'),
		]

	def __str__(self):
		return self.invoice_number
