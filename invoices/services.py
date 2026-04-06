from datetime import timedelta
from io import BytesIO

from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa

from .models import Invoice


def create_invoice_for_order(order):
    issue_date = timezone.localdate()
    due_date = issue_date + timedelta(days=30)
    invoice_number = f'MHD-{issue_date.year}-{order.pk:05d}'
    invoice, _ = Invoice.objects.get_or_create(
        order=order,
        defaults={
            'invoice_number': invoice_number,
            'issue_date': issue_date,
            'due_date': due_date,
            'amount': order.total_amount,
        },
    )
    return invoice


def render_invoice_pdf(invoice):
    template = get_template('invoices/pdf.html')
    html = template.render({'invoice': invoice})
    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)
    if pisa_status.err:
        return None
    return buffer.getvalue()