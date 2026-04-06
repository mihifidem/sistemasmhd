from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from distributors.decorators import approved_distributor_required

from .models import Invoice
from .services import render_invoice_pdf


@approved_distributor_required
def invoice_list(request):
    invoices = Invoice.objects.filter(order__distributor=request.user.distributor_profile).select_related('order')
    return render(request, 'invoices/list.html', {'invoices': invoices})


@approved_distributor_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('order'), pk=pk, order__distributor=request.user.distributor_profile)
    return render(request, 'invoices/detail.html', {'invoice': invoice})


@approved_distributor_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('order__distributor'), pk=pk, order__distributor=request.user.distributor_profile)
    pdf = render_invoice_pdf(invoice)
    if pdf is None:
        return HttpResponse('Unable to generate invoice PDF.', status=500)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_number}.pdf"'
    return response
