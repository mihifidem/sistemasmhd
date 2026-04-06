from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from blog.models import BlogPost
from products.models import Product
from support.models import FAQ


class Command(BaseCommand):
    help = 'Seed default MHD catalog, FAQ entries, and sample blog posts.'

    def handle(self, *args, **options):
        product_specs = [
            {
                'name': 'MHD Agua',
                'description': 'Magnetic device installed on water pipes to reduce limescale formation and protect boilers and hydraulic components.',
                'distributor_price': Decimal('20.00'),
                'public_price': Decimal('39.00'),
                'units_per_box': 20,
                'stock': 500,
                'active': True,
            },
            {
                'name': 'MHD Gas',
                'description': 'Magnetic device installed on gas boiler inputs to support cleaner combustion behavior and improved efficiency.',
                'distributor_price': Decimal('29.00'),
                'public_price': Decimal('55.00'),
                'units_per_box': 24,
                'stock': 350,
                'active': True,
            },
        ]

        for spec in product_specs:
            Product.objects.update_or_create(name=spec['name'], defaults=spec)

        faq_specs = [
            ('Does the device magnetize water?', 'No. The technology changes how minerals behave in circulation rather than permanently magnetizing the water.'),
            ('Does it work with hard water?', 'Yes. Hard-water installations are one of the main use cases for MHD Agua.'),
            ('How is it installed?', 'Qualified professionals install the devices inline on the relevant water or gas feed.'),
            ('How long does it last?', 'The devices are passive and designed for long service life with minimal maintenance.'),
        ]

        for index, (question, answer) in enumerate(faq_specs, start=1):
            FAQ.objects.update_or_create(
                question=question,
                defaults={
                    'answer': answer,
                    'display_order': index,
                    'is_active': True,
                },
            )

        User = get_user_model()
        author, _ = User.objects.get_or_create(
            username='mhd-editor',
            defaults={
                'email': 'editor@mhd-platform.com',
                'is_staff': True,
            },
        )

        posts = [
            {
                'title': 'Boiler maintenance strategies for scale-prone regions',
                'content': 'Boilers in hard-water regions face higher fouling rates, more service intervals, and lower heat-transfer efficiency. Preventive design choices matter.',
            },
            {
                'title': 'Why water hardness impacts energy efficiency',
                'content': 'Water hardness accelerates mineral buildup on heated surfaces, increasing operating cost and reducing system responsiveness over time.',
            },
            {
                'title': 'Combustion efficiency and boiler lifecycle performance',
                'content': 'Improving combustion consistency can reduce waste, lower stress on system components, and support better long-term reliability.',
            },
        ]

        for post in posts:
            BlogPost.objects.update_or_create(
                slug=slugify(post['title']),
                defaults={
                    'title': post['title'],
                    'author': author,
                    'content': post['content'],
                    'publish_date': timezone.now(),
                    'meta_title': post['title'],
                    'meta_description': post['content'][:155],
                    'is_published': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Seed data created or updated successfully.'))