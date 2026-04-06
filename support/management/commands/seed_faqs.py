"""
Management command: seed_faqs
Crea preguntas frecuentes por categoría, en español, orientadas al público final.
Uso: python manage.py seed_faqs [--clear]
"""
from django.core.management.base import BaseCommand
from support.models import FAQ

FAQS = [
    # ── Tecnología MHD ──────────────────────────────────────────────────────
    {
        'category': FAQ.Category.TECHNOLOGY,
        'question': '¿Qué es la tecnología MHD y cómo funciona en mi caldera?',
        'answer': (
            'MHD (Magnetohidrodinámica) aplica campos magnéticos controlados alrededor '
            'de las tuberías de agua y gas de tu caldera. Esto modifica el comportamiento '
            'de los minerales disueltos en el agua —principalmente calcio y magnesio— '
            'reduciendo su tendencia a adherirse a las superficies internas. '
            'El resultado es menos incrustación de cal y una combustión más estable, '
            'sin productos químicos ni obras.'
        ),
        'display_order': 1,
    },
    {
        'category': FAQ.Category.TECHNOLOGY,
        'question': '¿Necesito electricidad para que funcione el dispositivo?',
        'answer': (
            'No. Los dispositivos MHD son completamente pasivos: no necesitan corriente '
            'eléctrica, pilas ni ningún tipo de mantenimiento periódico. Funcionan '
            'mientras el agua o el gas circulan a través de la zona tratada.'
        ),
        'display_order': 2,
    },
    {
        'category': FAQ.Category.TECHNOLOGY,
        'question': '¿El dispositivo altera la composición química del agua que bebo?',
        'answer': (
            'No. La tecnología MHD no añade ni elimina sustancias del agua. '
            'Solo influye temporalmente en el comportamiento físico de los minerales '
            'mientras el agua está bajo el efecto del campo magnético. '
            'El agua sigue siendo apta para el consumo humano.'
        ),
        'display_order': 3,
    },
    {
        'category': FAQ.Category.TECHNOLOGY,
        'question': '¿Cuánto tiempo tarda en notarse el efecto?',
        'answer': (
            'Los resultados varían según la dureza del agua y el estado previo de la instalación. '
            'En general, los usuarios empiezan a notar mejoras —menos cal visible, '
            'mejor rendimiento de la caldera— entre el primer y el tercer mes de uso.'
        ),
        'display_order': 4,
    },
    {
        'category': FAQ.Category.TECHNOLOGY,
        'question': '¿Es compatible con cualquier tipo de caldera?',
        'answer': (
            'Sí. Los dispositivos MHD son compatibles con calderas de gas natural, '
            'propano, condensación y calefacción centralizada. Tu instalador comprobará '
            'el diámetro de tubería y el tipo de instalación antes de la puesta en marcha.'
        ),
        'display_order': 5,
    },

    # ── MHD Agua ─────────────────────────────────────────────────────────────
    {
        'category': FAQ.Category.MHD_AGUA,
        'question': '¿Qué problema resuelve MHD Agua en mi hogar?',
        'answer': (
            'Si vives en una zona de agua dura, la cal se acumula en el interior de la caldera, '
            'los radiadores y las tuberías. Esto reduce la transferencia de calor, '
            'aumenta el consumo de energía y acorta la vida útil del equipo. '
            'MHD Agua actúa sobre el agua de aporte para reducir esta adherencia de cal '
            'sin necesidad de sal ni cartuchos.'
        ),
        'display_order': 1,
    },
    {
        'category': FAQ.Category.MHD_AGUA,
        'question': '¿Dónde se instala MHD Agua?',
        'answer': (
            'Se instala en la tubería de entrada de agua fría de la caldera, '
            'antes del intercambiador de calor. La instalación la realiza un '
            'técnico cualificado y no requiere obras: solo conexión en línea a la tubería existente.'
        ),
        'display_order': 2,
    },
    {
        'category': FAQ.Category.MHD_AGUA,
        'question': '¿Necesita revisiones o recambios periódicos?',
        'answer': (
            'No. MHD Agua es un dispositivo pasivo sin piezas móviles ni consumibles. '
            'No requiere cambios de filtro, sal ni ningún tipo de reposición. '
            'Una vez instalado, funciona de forma continua sin intervención.'
        ),
        'display_order': 3,
    },
    {
        'category': FAQ.Category.MHD_AGUA,
        'question': '¿Puedo usarlo si tengo agua del pozo o agua muy dura?',
        'answer': (
            'Sí. MHD Agua está especialmente indicado para instalaciones con agua de dureza '
            'media-alta (a partir de 200 mg/l de carbonato cálcico). Si tu agua es de pozo, '
            'consulta con tu instalador para confirmar la idoneidad según el análisis del agua.'
        ),
        'display_order': 4,
    },
    {
        'category': FAQ.Category.MHD_AGUA,
        'question': '¿Reduce MHD Agua la cal que ya tengo acumulada?',
        'answer': (
            'Con el tiempo, los depósitos de cal existentes pueden ir reduciéndose '
            'al cambiar las condiciones de adherencia del mineral. Sin embargo, '
            'el efecto principal es preventivo: evita que se forme nueva cal. '
            'Si hay incrustaciones graves previas, tu técnico puede recomendar una limpieza previa.'
        ),
        'display_order': 5,
    },

    # ── MHD Gas ──────────────────────────────────────────────────────────────
    {
        'category': FAQ.Category.MHD_GAS,
        'question': '¿Qué hace MHD Gas en mi caldera de gas?',
        'answer': (
            'MHD Gas se instala en la tubería de entrada de gas de la caldera. '
            'Aplica un campo magnético sobre el flujo de gas para favorecer '
            'una combustión más homogénea y estable. Esto puede traducirse en '
            'una llama más regular, menos variaciones de temperatura y, en muchos casos, '
            'una reducción del consumo de gas.'
        ),
        'display_order': 1,
    },
    {
        'category': FAQ.Category.MHD_GAS,
        'question': '¿Es seguro instalar un dispositivo en la tubería de gas?',
        'answer': (
            'Sí. La instalación la realiza siempre un técnico habilitado en gas, '
            'siguiendo la normativa vigente. El dispositivo no interviene químicamente '
            'en el gas ni altera su presión: es una pieza pasiva que rodea la tubería.'
        ),
        'display_order': 2,
    },
    {
        'category': FAQ.Category.MHD_GAS,
        'question': '¿MHD Gas reduce las averías de la caldera?',
        'answer': (
            'Una combustión más estable reduce el estrés térmico en el quemador y el '
            'intercambiador. Muchos usuarios reportan menos errores de encendido '
            'y menos llamadas al servicio técnico tras la instalación, aunque los '
            'resultados dependen del estado previo del equipo.'
        ),
        'display_order': 3,
    },
    {
        'category': FAQ.Category.MHD_GAS,
        'question': '¿Es compatible con calderas de condensación?',
        'answer': (
            'Sí. MHD Gas es compatible con calderas de condensación, '
            'que son las más eficientes del mercado actualmente. '
            'Tu instalador verificará el diámetro de la tubería de gas y '
            'la posición óptima de montaje.'
        ),
        'display_order': 4,
    },
    {
        'category': FAQ.Category.MHD_GAS,
        'question': '¿Puedo combinar MHD Agua y MHD Gas en la misma instalación?',
        'answer': (
            'Sí, y es la combinación más habitual. MHD Agua actúa sobre el circuito '
            'hidráulico reduciendo la cal, mientras que MHD Gas mejora la combustión. '
            'Juntos ofrecen una protección integral de la caldera.'
        ),
        'display_order': 5,
    },

    # ── Servicio Técnico ─────────────────────────────────────────────────────
    {
        'category': FAQ.Category.TECH_SERVICE,
        'question': '¿Quién instala los dispositivos MHD?',
        'answer': (
            'La instalación la realiza uno de nuestros distribuidores e instaladores '
            'autorizados. Puedes encontrar el más cercano a tu domicilio usando el '
            'buscador de instaladores disponible en esta web.'
        ),
        'display_order': 1,
    },
    {
        'category': FAQ.Category.TECH_SERVICE,
        'question': '¿Cuánto tiempo dura la instalación?',
        'answer': (
            'La instalación estándar de uno o dos dispositivos suele completarse '
            'en menos de dos horas. No requiere corte de suministro prolongado '
            'ni obras en la pared.'
        ),
        'display_order': 2,
    },
    {
        'category': FAQ.Category.TECH_SERVICE,
        'question': '¿Qué garantía tienen los dispositivos?',
        'answer': (
            'Los dispositivos MHD cuentan con garantía del fabricante. '
            'Consulta con tu instalador autorizado las condiciones específicas '
            'de garantía y el proceso de reclamación en caso de incidencia.'
        ),
        'display_order': 3,
    },
    {
        'category': FAQ.Category.TECH_SERVICE,
        'question': '¿Qué hago si tengo una avería o duda después de la instalación?',
        'answer': (
            'Contacta directamente con el instalador que realizó la puesta en marcha: '
            'es tu punto de soporte más rápido. Si necesitas escalar la incidencia, '
            'puedes usar el formulario de contacto de esta web o el chat de soporte.'
        ),
        'display_order': 4,
    },
    {
        'category': FAQ.Category.TECH_SERVICE,
        'question': '¿Se puede desinstalar si cambio de caldera?',
        'answer': (
            'Sí. Los dispositivos MHD no están soldados ni pegados a la tubería. '
            'Un técnico puede retirarlos y volver a instalarlos en la nueva caldera '
            'sin dañar ningún componente.'
        ),
        'display_order': 5,
    },
]


class Command(BaseCommand):
    help = 'Crea preguntas frecuentes por categoría en español para público final.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Eliminar todas las FAQs antes de insertar.')

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = FAQ.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Eliminadas {deleted} FAQs.'))

        created = 0
        for data in FAQS:
            _, was_created = FAQ.objects.get_or_create(
                question=data['question'],
                defaults={
                    'answer': data['answer'],
                    'category': data['category'],
                    'display_order': data['display_order'],
                    'is_active': True,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Listo. {created} FAQs nuevas creadas ({len(FAQS) - created} ya existían).'))
