from django.http import JsonResponse
from django.shortcuts import render

from .models import FAQ


CHATBOT_RESPONSES = {
    'magnetize water': 'The device does not permanently magnetize water. It changes how minerals behave while the water flows through the treated section.',
    'hard water': 'Yes. MHD Agua is designed for hard-water environments where limescale formation is a recurring maintenance problem.',
    'installed': 'The devices are installed inline by qualified installers. MHD Agua mounts on water pipes and MHD Gas mounts on the gas boiler input.',
    'last': 'The devices are passive and designed for long operating life with minimal maintenance when installed correctly.',
    'combustion': 'MHD Gas is positioned to support cleaner combustion behavior and more stable boiler efficiency over time.',
    'limescale': 'MHD Agua helps reduce limescale adhesion, which can limit scaling inside boilers and hydraulic components.',
}


def faq_list(request):
    faqs = FAQ.objects.filter(is_active=True)

    # Agrupar por categoría manteniendo orden de choices
    categories = []
    for value, label in FAQ.Category.choices:
        qs = [f for f in faqs if f.category == value]
        if qs:
            categories.append({'value': value, 'label': label, 'faqs': qs})

    return render(request, 'support/faq.html', {'categories': categories, 'faqs': faqs})


def chatbot_response(request):
    question = request.GET.get('q', '').lower()
    answer = 'Los dispositivos MHD están diseñados para reducir la cal, mejorar la eficiencia de la caldera y encajar fácilmente en instalaciones existentes.'
    for keyword, response in CHATBOT_RESPONSES.items():
        if keyword in question:
            answer = response
            break
    return JsonResponse({'answer': answer})
