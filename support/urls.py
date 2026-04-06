from django.urls import path

from . import views

app_name = 'support'

urlpatterns = [
    path('faq/', views.faq_list, name='faq'),
    path('assistant/', views.chatbot_response, name='assistant'),
]