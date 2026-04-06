from decimal import Decimal

from django.db import models

from distributors.models import Distributor
from products.models import Product


class Order(models.Model):
	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		CONFIRMED = 'confirmed', 'Confirmed'
		SHIPPED = 'shipped', 'Shipped'
		DELIVERED = 'delivered', 'Delivered'

	distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE, related_name='orders')
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	early_payment_discount = models.BooleanField(
		default=False,
		verbose_name='Descuento pronto pago',
		help_text='10 % de descuento por pago al contado en el momento del pedido.',
	)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'Order #{self.pk}'

	def refresh_total(self):
		total = sum(item.line_total for item in self.items.all())
		self.total_amount = total
		self.save(update_fields=['total_amount'])


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return f'{self.product.name} x {self.quantity}'

	@property
	def line_total(self):
		return self.price * self.quantity
