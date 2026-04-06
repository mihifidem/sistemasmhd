from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('recursos/', views.resources, name='resources'),
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('<slug:slug>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
]