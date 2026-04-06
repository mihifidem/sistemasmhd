from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'distributor', 'status', 'total_amount', 'early_payment_discount', 'created_at')
	list_filter = ('status', 'early_payment_discount', 'created_at')
	search_fields = ('id', 'distributor__company_name')
	inlines = [OrderItemInline]
