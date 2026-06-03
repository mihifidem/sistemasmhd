
from django.urls import path

from . import views

app_name = 'distributors'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('registration-status/', views.registration_status, name='registration_status'),
    path('technicians/login/', views.technician_login, name='technician_login'),
    path('technicians/resources/', views.technician_resources, name='technician_resources'),
    path('technicians/logout/', views.technician_logout, name='technician_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resources/', views.resources, name='resources'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/technician-access/', views.edit_technician_access, name='edit_technician_access'),
    path('profile/generate-bio/', views.generate_bio, name='generate_bio'),
    path('profile/geocode/', views.geocode_address, name='geocode_address'),
    path('installers/', views.installer_locator, name='installer_locator'),
    path('search.json', views.distributor_search_json, name='search_json'),
    path('map/', views.distributor_map, name='map'),
]