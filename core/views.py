from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from blog.models import BlogPost
from distributors.models import Distributor
from invoices.models import Invoice
from orders.models import Order
from products.models import Product
from support.models import FAQ


def home(request):
	context = {
		'featured_products': Product.objects.filter(active=True)[:2],
		'latest_posts': BlogPost.objects.filter(is_published=True, distributors_only=False).order_by('-publish_date')[:3],
		'faqs': FAQ.objects.filter(is_active=True)[:4],
		'testimonials': [
			{
				'quote': 'Llevamos dos años sin apenas avisos por incrustaciones de cal. La caldera funciona mucho mejor y los clientes están muy contentos.',
				'author': 'Marta Soler',
				'role': 'Cliente final · Propietaria de vivienda, Valencia',
			},
			{
				'quote': 'Desde que instalamos MHD Agua en la comunidad, el consumo de gas ha bajado y no hemos tenido que limpiar el circuito.',
				'author': 'Javier Pons',
				'role': 'Cliente final · Presidente de comunidad de vecinos, Barcelona',
			},
			{
				'quote': 'Mi caldera de gas tenía problemas de combustión frecuentes. Con MHD Gas la llama es más estable y no ha vuelto a dar errores.',
				'author': 'Rosa Jiménez',
				'role': 'Cliente final · Vivienda unifamiliar, Madrid',
			},
			{
				'quote': 'Hemos reducido visitas de mantenimiento por cal en más de un 40 %. La propuesta de valor para nuestros clientes es muy clara.',
				'author': 'Raúl Medina',
				'role': 'Distribuidor regional · Madrid y Castilla-La Mancha',
			},
			{
				'quote': 'La respuesta de combustión en calderas antiguas mejoró de forma visible tras instalar MHD Gas. Los clientes lo notan desde el primer mes.',
				'author': 'Elena Torres',
				'role': 'Distribuidora · Directora técnica, Sevilla',
			},
			{
				'quote': 'El producto es muy fácil de instalar. Los proyectos van rápido y los márgenes son sanos. Lo recomendamos a toda nuestra red.',
				'author': 'Carlos Vega',
				'role': 'Instalador asociado · Bilbao',
			},
		],
	}
	return render(request, 'core/home.html', context)


def how_it_works(request):
	return render(request, 'core/how_it_works.html')


@staff_member_required
def admin_dashboard(request):
	order_totals = Order.objects.aggregate(total=Sum('total_amount'))
	context = {
		'distributor_count': Distributor.objects.count(),
		'pending_distributors': Distributor.objects.filter(status=Distributor.Status.PENDING).count(),
		'active_products': Product.objects.filter(active=True).count(),
		'unpaid_invoices': Invoice.objects.filter(status=Invoice.Status.PENDING).count(),
		'order_volume': order_totals['total'] or 0,
		'recent_orders': Order.objects.select_related('distributor').order_by('-created_at')[:8],
		'top_distributors': Distributor.objects.annotate(order_count=Count('orders')).order_by('-order_count')[:5],
	}
	return render(request, 'core/admin_dashboard.html', context)


SYSTEM_PROMPT = """Eres el asistente virtual de MHD, una empresa especializada en tecnología magnetohidrodinámica (MHD) para el tratamiento del agua y la mejora de la combustión en calderas.

Responde únicamente preguntas relacionadas con:
- Productos MHD Agua y MHD Gas
- Tecnología MHD y cómo funciona
- Prevención de incrustaciones de cal
- Eficiencia energética y ahorro en calderas
- Instalación y mantenimiento de los dispositivos
- Distribuidores y cómo convertirse en distribuidor

Si te preguntan algo fuera de estos temas, indica amablemente que solo puedes ayudar con temas relacionados con MHD.

Sé conciso, profesional y amable. Responde en el mismo idioma en que te escriban."""


@require_POST
def chat(request):
    import json
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Petición inválida.'}, status=400)

    if not message:
        return JsonResponse({'error': 'Mensaje vacío.'}, status=400)

    if len(message) > 500:
        return JsonResponse({'error': 'Mensaje demasiado largo.'}, status=400)

    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return JsonResponse({'error': 'El chatbot no está configurado. Contacta con el administrador.'}, status=503)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': message},
            ],
            max_tokens=400,
            temperature=0.5,
        )
        reply = response.choices[0].message.content.strip()
        return JsonResponse({'reply': reply})
    except Exception as e:
        import logging
        logging.getLogger(__name__).error('Chat error: %s', e)
        return JsonResponse({'error': str(e)}, status=502)
