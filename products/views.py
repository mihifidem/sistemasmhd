from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from distributors.decorators import approved_distributor_required
from orders.cart import Cart

from .forms import CartAddForm
from .models import Product, Resource


@approved_distributor_required
def catalog(request):
    products = Product.objects.filter(active=True)
    return render(request, 'products/catalog.html', {'products': products})


def product_detail(request, slug):
    product = Product.objects.filter(slug=slug, active=True).first()
    if not product and slug == 'mhd-agua2':
        return render(request, 'products/mhd_agua_detail.html')
    if not product and slug == 'mhd-gas2':
        return render(request, 'products/mhd_gas_detail.html')
    if not product:
        raise Http404('Product not found')
    form = CartAddForm() if request.user.is_authenticated else None
    return render(request, 'products/detail.html', {'product': product, 'form': form})


@approved_distributor_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    form = CartAddForm(request.POST)
    if form.is_valid():
        distributor = request.user.distributor_profile
        tier_price = product.get_tier_price(distributor.price_tier)
        Cart(request).add(product, form.cleaned_data['quantity'], price=tier_price)
        messages.success(request, f'{product.name} added to your cart.')
    return redirect('orders:cart_summary')


def resources(request):
    rtype = request.GET.get('tipo', '')
    qs = Resource.objects.filter(active=True, is_public=True).select_related('product')
    if rtype:
        qs = qs.filter(resource_type=rtype)
    types = Resource.ResourceType.choices
    return render(request, 'products/resources.html', {
        'resources': qs,
        'types': types,
        'active_type': rtype,
    })
