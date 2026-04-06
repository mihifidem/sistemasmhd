from django.contrib import admin
from django.utils.html import format_html

from .models import Distributor


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
	list_display = ('company_name', 'company_type', 'province', 'price_tier', 'status_badge', 'created_at')
	list_filter = ('company_type', 'status', 'province')
	search_fields = ('company_name', 'cif', 'contact_person', 'email')
	autocomplete_fields = ('user',)
	actions = ('approve_distributors',)
	fieldsets = (
		(None, {'fields': ('user', 'company_name', 'cif', 'contact_person', 'email', 'phone', 'company_type', 'status', 'price_tier', 'services_offered', 'bio')}),
		('Ubicación', {'fields': ('address', 'city', 'province', 'postal_code', 'latitude', 'longitude')}),
	)

	@admin.display(description='Status')
	def status_badge(self, obj):
		color = {
			Distributor.Status.PENDING: '#f59e0b',
			Distributor.Status.APPROVED: '#22c55e',
			Distributor.Status.REJECTED: '#fb7185',
		}[obj.status]
		return format_html('<strong style="color: {}">{}</strong>', color, obj.get_status_display())

	@admin.action(description='Approve selected distributors')
	def approve_distributors(self, request, queryset):
		for distributor in queryset.exclude(status=Distributor.Status.APPROVED):
			distributor.status = Distributor.Status.APPROVED
			distributor.save()
