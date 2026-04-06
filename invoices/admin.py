from django.contrib import admin

from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = ('invoice_number', 'order', 'issue_date', 'due_date', 'amount', 'status')
	list_filter = ('status', 'issue_date', 'due_date')
	search_fields = ('invoice_number', 'order__distributor__company_name')
