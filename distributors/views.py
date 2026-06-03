from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from invoices.models import Invoice
from orders.models import Order
from products.models import Resource

from .decorators import approved_distributor_required, technician_portal_required
from .forms import DistributorProfileForm, DistributorRegistrationForm, TechnicianPortalAccessForm
from .models import Distributor


def _build_grouped_private_resources():
    resource_types = [
        ('video', 'Vídeos'),
        ('audio', 'Podcasts'),
        ('pdf', 'PDFs'),
        ('infographic', 'Infografías'),
        ('link', 'Presentaciones y enlaces'),
    ]
    private_resources = Resource.objects.filter(active=True, is_public=False).select_related('product').order_by('order', '-created_at')
    grouped_resources = []
    for resource_type, label in resource_types:
        items = [resource for resource in private_resources if resource.resource_type == resource_type]
        grouped_resources.append({
            'type': resource_type,
            'label': label,
            'items': items,
            'has_items': bool(items),
        })
    return grouped_resources


def register(request):
    if request.user.is_authenticated and hasattr(request.user, 'distributor_profile'):
        return redirect('distributors:registration_status')

    if request.method == 'POST':
        form = DistributorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration received. Your account is pending approval.')
            return redirect('distributors:registration_status')
    else:
        form = DistributorRegistrationForm()
    return render(request, 'distributors/register.html', {'form': form})


def registration_status(request):
    profile = getattr(request.user, 'distributor_profile', None) if request.user.is_authenticated else None
    return render(request, 'distributors/registration_status.html', {'profile': profile})


@approved_distributor_required
def dashboard(request):
    distributor = request.user.distributor_profile
    recent_orders = distributor.orders.select_related().prefetch_related('items__product')[:5]
    private_resources = Resource.objects.filter(active=True, is_public=False).select_related('product').order_by('order', '-created_at')
    context = {
        'recent_orders': recent_orders,
        'pending_invoices': Invoice.objects.filter(order__distributor=distributor, status=Invoice.Status.PENDING),
        'order_history': distributor.orders.prefetch_related('items__product')[:10],
        'distributor': distributor,
        'activity_count': Order.objects.filter(distributor=distributor).count(),
        'private_resources': private_resources,
    }
    return render(request, 'distributors/dashboard.html', context)


@approved_distributor_required
def resources(request):
    return render(request, 'distributors/resources.html', {
        'grouped_resources': _build_grouped_private_resources(),
    })


def technician_login(request):
    if request.session.get('technician_distributor_id'):
        return redirect('distributors:technician_resources')

    error = ''
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip().lower()
        password = request.POST.get('password') or ''

        distributor = Distributor.objects.filter(
            technician_portal_username__iexact=username,
            status=Distributor.Status.APPROVED,
        ).first()

        if distributor and distributor.check_technician_password(password):
            request.session['technician_distributor_id'] = distributor.pk
            request.session['technician_distributor_name'] = distributor.company_name
            return redirect('distributors:technician_resources')

        error = 'Usuario o contraseña incorrectos.'

    return render(request, 'distributors/technician_login.html', {'error': error})


@technician_portal_required
def technician_resources(request):
    return render(request, 'distributors/technician_resources.html', {
        'distributor': request.technician_distributor,
        'grouped_resources': _build_grouped_private_resources(),
    })


def technician_logout(request):
    request.session.pop('technician_distributor_id', None)
    request.session.pop('technician_distributor_name', None)
    return redirect('distributors:technician_login')


@approved_distributor_required
def profile(request):
    distributor = request.user.distributor_profile
    form = DistributorProfileForm(instance=distributor)
    technician_form = TechnicianPortalAccessForm(instance=distributor)
    return render(request, 'distributors/profile.html', {
        'distributor': distributor,
        'form': form,
        'technician_form': technician_form,
    })


@approved_distributor_required
def edit_profile(request):
    distributor = request.user.distributor_profile
    if request.method == 'POST':
        form = DistributorProfileForm(request.POST, instance=distributor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('distributors:profile')
    else:
        form = DistributorProfileForm(instance=distributor)
    technician_form = TechnicianPortalAccessForm(instance=distributor)
    return render(request, 'distributors/profile.html', {
        'distributor': distributor,
        'form': form,
        'technician_form': technician_form,
    })


@approved_distributor_required
def edit_technician_access(request):
    distributor = request.user.distributor_profile
    if request.method != 'POST':
        return redirect('distributors:profile')

    technician_form = TechnicianPortalAccessForm(request.POST, instance=distributor)
    if technician_form.is_valid():
        technician_form.save()
        messages.success(request, 'Credenciales del panel técnico actualizadas correctamente.')
        return redirect('distributors:profile')

    form = DistributorProfileForm(instance=distributor)
    return render(request, 'distributors/profile.html', {
        'distributor': distributor,
        'form': form,
        'technician_form': technician_form,
    })


@approved_distributor_required
def geocode_address(request):
    import json
    import urllib.parse
    import urllib.request

    address     = request.GET.get('address', '').strip()
    city        = request.GET.get('city', '').strip()
    province    = request.GET.get('province', '').strip()
    postal_code = request.GET.get('postal_code', '').strip()

    parts = [p for p in [address, city, province, postal_code, 'España'] if p]
    if len(parts) <= 1:
        return JsonResponse({'error': 'Introduce al menos una parte de la dirección'}, status=400)

    query = ', '.join(parts)
    params = urllib.parse.urlencode({'q': query, 'format': 'json', 'limit': 1})
    url = 'https://nominatim.openstreetmap.org/search?' + params
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'MHDPlatform/1.0 distributor-geocoder'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        if data:
            lat = round(float(data[0]['lat']), 6)
            lng = round(float(data[0]['lon']), 6)
            return JsonResponse({'lat': lat, 'lng': lng})
        return JsonResponse({'error': 'Dirección no encontrada'}, status=404)
    except Exception:
        return JsonResponse({'error': 'Error al geocodificar'}, status=503)


@require_POST
@approved_distributor_required
def generate_bio(request):
    import json
    from django.conf import settings
    distributor = request.user.distributor_profile
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return JsonResponse({'error': 'IA no configurada. Contacta con el administrador.'}, status=503)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = {}
    company_name    = data.get('company_name', distributor.company_name)
    company_type    = distributor.get_company_type_display()
    province        = data.get('province', distributor.province)
    city            = data.get('city', distributor.city)
    services        = data.get('services_offered', distributor.services_offered)
    prompt = (
        f"Eres un redactor profesional de perfiles comerciales en español. "
        f"Escribe una presentación/bio breve (3-4 frases, máximo 120 palabras) para un distribuidor oficial de MHD Platform "
        f"con estos datos:\n"
        f"- Empresa: {company_name}\n"
        f"- Tipo: {company_type}\n"
        f"- Ubicación: {city}, {province}\n"
        f"- Servicios: {services or 'no especificados'}\n\n"
        f"El tono debe ser profesional, cercano y orientado a captar clientes. "
        f"No uses asteriscos ni markdown. Solo texto plano."
    )
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=200,
            temperature=0.7,
        )
        bio = response.choices[0].message.content.strip()
        return JsonResponse({'bio': bio})
    except Exception as e:
        import logging
        logging.getLogger(__name__).error('generate_bio error: %s', e)
        return JsonResponse({'error': str(e)}, status=502)


def installer_locator(request):
    installers = Distributor.objects.filter(status=Distributor.Status.APPROVED).order_by('company_name')
    return render(request, 'distributors/installer_locator.html', {'installers': installers})


def distributor_search_json(request):
    qs = Distributor.objects.filter(status=Distributor.Status.APPROVED).order_by('company_name')
    data = [
        {
            'company_name': d.company_name,
            'province': d.province,
            'city': d.city,
            'phone': d.phone,
            'email': d.email,
            'services_offered': d.services_offered,
            'company_type': d.get_company_type_display(),
            'latitude': str(d.latitude) if d.latitude is not None else None,
            'longitude': str(d.longitude) if d.longitude is not None else None,
        }
        for d in qs
    ]
    return JsonResponse(data, safe=False)


def distributor_map(request):
    import folium
    qs = Distributor.objects.filter(
        status=Distributor.Status.APPROVED,
        latitude__isnull=False,
        longitude__isnull=False,
    )
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=6, tiles='CartoDB positron')
    for d in qs:
        folium.Marker(
            location=[float(d.latitude), float(d.longitude)],
            popup=folium.Popup(
                f"<b>{d.company_name}</b><br>{d.city}, {d.province}<br>"
                f"<a href='tel:{d.phone}'>{d.phone}</a><br>{d.email}",
                max_width=260,
            ),
            tooltip=d.company_name,
            icon=folium.Icon(color='blue', icon='info-sign'),
        ).add_to(m)
    return HttpResponse(m.get_root().render())
