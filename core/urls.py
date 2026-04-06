from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('chat/', views.chat, name='chat'),
]