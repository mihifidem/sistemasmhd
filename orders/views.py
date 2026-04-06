from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from distributors.decorators import approved_distributor_required
from invoices.services import create_invoice_for_order
from products.models import Product

from .cart import Cart
from .models import Order, OrderItem


@approved_distributor_required
def cart_summary(request):
    return render(request, 'orders/cart_summary.html', {'cart_items': list(Cart(request))})


@approved_distributor_required
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    quantity = max(1, int(request.POST.get('quantity', 1)))
    Cart(request).add(product, quantity, override_quantity=True)
    messages.success(request, 'Cart updated.')
    return redirect('orders:cart_summary')


@approved_distributor_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Cart(request).remove(product)
    messages.success(request, 'Product removed from cart.')
    return redirect('orders:cart_summary')


@approved_distributor_required
@transaction.atomic
def submit_order(request):
    cart = Cart(request)
    items = list(cart)
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('products:catalog')

    distributor = request.user.distributor_profile
    order = Order.objects.create(distributor=distributor, total_amount=cart.get_total_price())
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price'],
        )
    order.refresh_total()
    create_invoice_for_order(order)
    cart.clear()

    send_mail(
        subject=f'MHD order confirmation #{order.pk}',
        message=(
            f'Hello {distributor.contact_person},\n\n'
            f'We have received your order #{order.pk} for {order.total_amount} EUR.\n'
            'We will confirm shipping details shortly.\n\n'
            'Regards,\nMHD Team'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[distributor.email],
        fail_silently=True,
    )
    messages.success(request, f'Order #{order.pk} submitted successfully.')
    return redirect('orders:detail', pk=order.pk)


@approved_distributor_required
@transaction.atomic
def new_order(request):
    distributor = request.user.distributor_profile
    products = list(Product.objects.filter(active=True).order_by('name'))
    for _p in products:
        _p.effective_price = _p.get_tier_price(distributor.price_tier)
    if request.method == 'POST':
        items_data = []
        for product in products:
            raw = request.POST.get(f'qty_{product.id}', '0').strip()
            try:
                boxes = max(0, int(raw))
            except ValueError:
                boxes = 0
            if boxes > 0:
                items_data.append((product, boxes))

        if not items_data:
            messages.warning(request, 'Selecciona al menos un producto antes de confirmar el pedido.')
            return render(request, 'orders/new_order.html', {'products': products, 'distributor': distributor})

        early_payment = request.POST.get('early_payment') == '1'
        discount_factor = Decimal('0.90') if early_payment else Decimal('1.00')

        order = Order.objects.create(
            distributor=distributor,
            total_amount=0,
            early_payment_discount=early_payment,
        )
        for product, boxes in items_data:
            price_per_box = (product.effective_price * product.units_per_box * discount_factor).quantize(Decimal('0.01'))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=boxes,
                price=price_per_box,
            )
        order.refresh_total()
        create_invoice_for_order(order)

        discount_note = ' (con descuento pronto pago del 10 %)' if early_payment else ''

        send_mail(
            subject=f'MHD — Confirmación de pedido #{order.pk}',
            message=(
                f'Hola {distributor.contact_person},\n\n'
                f'Hemos recibido tu pedido #{order.pk} por un total de {order.total_amount} €{discount_note}.\n'
                'Nuestro equipo lo confirmará y te informará de los detalles de envío en breve.\n\n'
                'Gracias,\nEquipo MHD'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[distributor.email],
            fail_silently=True,
        )
        messages.success(request, f'Pedido #{order.pk} enviado correctamente.')
        return redirect('orders:detail', pk=order.pk)

    return render(request, 'orders/new_order.html', {'products': products, 'distributor': distributor})


@approved_distributor_required
def order_history(request):
    orders = request.user.distributor_profile.orders.prefetch_related('items__product')
    return render(request, 'orders/history.html', {'orders': orders})


@approved_distributor_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), pk=pk, distributor=request.user.distributor_profile)
    return render(request, 'orders/detail.html', {'order': order})
