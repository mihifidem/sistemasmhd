from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('nuevo/', views.new_order, name='new_order'),
    path('cart/', views.cart_summary, name='cart_summary'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('submit/', views.submit_order, name='submit_order'),
    path('history/', views.order_history, name='order_history'),
    path('<int:pk>/', views.order_detail, name='detail'),
]