"""
Management command: seed_distributors
Creates 100 fake approved distributors spread across Spanish provinces.
Usage: python manage.py seed_distributors [--clear]
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from distributors.models import Distributor

# fmt: off
# (province, city, lat, lon, postal_code)
LOCATIONS = [
    # Álava
    ("Álava", "Vitoria-Gasteiz",  42.8467, -2.6727, "01001"),
    ("Álava", "Llodio",            43.1423, -2.9635, "01400"),
    # Albacete
    ("Albacete", "Albacete",       38.9942, -1.8585, "02001"),
    ("Albacete", "Hellín",         38.5166, -1.7029, "02400"),
    # Alicante
    ("Alicante", "Alicante",       38.3452, -0.4815, "03001"),
    ("Alicante", "Benidorm",       38.5376,  0.1343, "03501"),
    ("Alicante", "Elche",          38.2669, -0.6985, "03201"),
    # Almería
    ("Almería", "Almería",         36.8381, -2.4597, "04001"),
    ("Almería", "Roquetas de Mar", 36.7636, -2.6148, "04740"),
    # Asturias
    ("Asturias", "Oviedo",         43.3614, -5.8496, "33001"),
    ("Asturias", "Gijón",          43.5328, -5.6613, "33201"),
    ("Asturias", "Avilés",         43.5569, -5.9249, "33400"),
    # Ávila
    ("Ávila", "Ávila",             40.6567, -4.6838, "05001"),
    # Badajoz
    ("Badajoz", "Badajoz",         38.8794, -6.9706, "06001"),
    ("Badajoz", "Mérida",          38.9154, -6.3446, "06800"),
    # Barcelona
    ("Barcelona", "Barcelona",     41.3851,  2.1734, "08001"),
    ("Barcelona", "Badalona",      41.4500,  2.2473, "08911"),
    ("Barcelona", "Terrassa",      41.5634,  2.0092, "08221"),
    ("Barcelona", "Sabadell",      41.5437,  2.1074, "08201"),
    ("Barcelona", "Mataró",        41.5374,  2.4449, "08301"),
    # Burgos
    ("Burgos", "Burgos",           42.3440, -3.6969, "09001"),
    # Cáceres
    ("Cáceres", "Cáceres",         39.4753, -6.3724, "10001"),
    # Cádiz
    ("Cádiz", "Cádiz",             36.5271, -6.2886, "11001"),
    ("Cádiz", "Jerez de la Frontera", 36.6864, -6.1376, "11401"),
    ("Cádiz", "Algeciras",         36.1289, -5.4535, "11201"),
    # Cantabria
    ("Cantabria", "Santander",     43.4623, -3.8099, "39001"),
    ("Cantabria", "Torrelavega",   43.3527, -4.0487, "39300"),
    # Castellón
    ("Castellón", "Castellón de la Plana", 39.9864, -0.0513, "12001"),
    # Ciudad Real
    ("Ciudad Real", "Ciudad Real", 38.9848, -3.9274, "13001"),
    ("Ciudad Real", "Puertollano", 38.6868, -4.1088, "13500"),
    # Córdoba
    ("Córdoba", "Córdoba",         37.8882, -4.7794, "14001"),
    ("Córdoba", "Lucena",          37.4083, -4.4862, "14900"),
    # A Coruña
    ("A Coruña", "A Coruña",       43.3623, -8.4115, "15001"),
    ("A Coruña", "Santiago de Compostela", 42.8782, -8.5448, "15701"),
    ("A Coruña", "Ferrol",         43.4842, -8.2315, "15401"),
    # Cuenca
    ("Cuenca", "Cuenca",           40.0704, -2.1374, "16001"),
    # Girona
    ("Girona", "Girona",           41.9794,  2.8214, "17001"),
    ("Girona", "Figueres",         42.2675,  2.9612, "17600"),
    # Granada
    ("Granada", "Granada",         37.1773, -3.5986, "18001"),
    ("Granada", "Motril",          36.7455, -3.5186, "18600"),
    # Guadalajara
    ("Guadalajara", "Guadalajara", 40.6321, -3.1656, "19001"),
    # Guipúzcoa
    ("Guipúzcoa", "Donostia-San Sebastián", 43.3183, -1.9812, "20001"),
    ("Guipúzcoa", "Irún",          43.3392, -1.7888, "20301"),
    # Huelva
    ("Huelva", "Huelva",           37.2614, -6.9447, "21001"),
    # Huesca
    ("Huesca", "Huesca",           42.1401, -0.4089, "22001"),
    # Jaén
    ("Jaén", "Jaén",               37.7796, -3.7849, "23001"),
    ("Jaén", "Linares",            38.0895, -3.6358, "23700"),
    # León
    ("León", "León",               42.5987, -5.5671, "24001"),
    ("León", "Ponferrada",         42.5461, -6.5983, "24400"),
    # Lleida
    ("Lleida", "Lleida",           41.6176,  0.6200, "25001"),
    # La Rioja
    ("La Rioja", "Logroño",        42.4667, -2.4500, "26001"),
    # Lugo
    ("Lugo", "Lugo",               43.0097, -7.5568, "27001"),
    # Madrid
    ("Madrid", "Madrid",           40.4168, -3.7038, "28001"),
    ("Madrid", "Alcalá de Henares", 40.4820, -3.3640, "28801"),
    ("Madrid", "Leganés",          40.3280, -3.7631, "28911"),
    ("Madrid", "Getafe",           40.3059, -3.7326, "28901"),
    ("Madrid", "Móstoles",         40.3224, -3.8644, "28930"),
    # Málaga
    ("Málaga", "Málaga",           36.7213, -4.4214, "29001"),
    ("Málaga", "Marbella",         36.5100, -4.8824, "29601"),
    ("Málaga", "Fuengirola",       36.5392, -4.6249, "29640"),
    # Murcia
    ("Murcia", "Murcia",           37.9922, -1.1307, "30001"),
    ("Murcia", "Cartagena",        37.6054, -0.9862, "30200"),
    ("Murcia", "Lorca",            37.6714, -1.6978, "30800"),
    # Navarra
    ("Navarra", "Pamplona",        42.8169, -1.6432, "31001"),
    ("Navarra", "Tudela",          42.0614, -1.6067, "31500"),
    # Ourense
    ("Ourense", "Ourense",         42.3440, -7.8659, "32001"),
    # Palencia
    ("Palencia", "Palencia",       42.0096, -4.5288, "34001"),
    # Palmas (Las)
    ("Las Palmas", "Las Palmas de Gran Canaria", 28.1248, -15.4300, "35001"),
    ("Las Palmas", "Arrecife",     28.9635, -13.5477, "35500"),
    # Pontevedra
    ("Pontevedra", "Vigo",         42.2314, -8.7124, "36201"),
    ("Pontevedra", "Pontevedra",   42.4336, -8.6478, "36001"),
    # Salamanca
    ("Salamanca", "Salamanca",     40.9701, -5.6635, "37001"),
    # S/C de Tenerife
    ("Santa Cruz de Tenerife", "Santa Cruz de Tenerife", 28.4636, -16.2518, "38001"),
    ("Santa Cruz de Tenerife", "San Cristóbal de La Laguna", 28.4853, -16.3180, "38200"),
    # Segovia
    ("Segovia", "Segovia",         40.9429, -4.1088, "40001"),
    # Sevilla
    ("Sevilla", "Sevilla",         37.3891, -5.9845, "41001"),
    ("Sevilla", "Dos Hermanas",    37.2961, -5.9204, "41701"),
    ("Sevilla", "Alcalá de Guadaíra", 37.3382, -5.8439, "41500"),
    # Soria
    ("Soria", "Soria",             41.7642, -2.4647, "42001"),
    # Tarragona
    ("Tarragona", "Tarragona",     41.1189,  1.2445, "43001"),
    ("Tarragona", "Reus",          41.1559,  1.1046, "43201"),
    # Teruel
    ("Teruel", "Teruel",           40.3456, -1.1065, "44001"),
    # Toledo
    ("Toledo", "Toledo",           39.8628, -4.0273, "45001"),
    ("Toledo", "Talavera de la Reina", 39.9616, -4.8310, "45600"),
    # Valencia
    ("Valencia", "Valencia",       39.4699, -0.3763, "46001"),
    ("Valencia", "Torrent",        39.4355, -0.4671, "46900"),
    ("Valencia", "Gandía",         38.9697, -0.1774, "46700"),
    # Valladolid
    ("Valladolid", "Valladolid",   41.6523, -4.7245, "47001"),
    # Vizcaya
    ("Vizcaya", "Bilbao",          43.2630, -2.9350, "48001"),
    ("Vizcaya", "Barakaldo",       43.2954, -2.9912, "48901"),
    ("Vizcaya", "Getxo",           43.3563, -3.0074, "48990"),
    # Zamora
    ("Zamora", "Zamora",           41.5034, -5.7448, "49001"),
    # Zaragoza
    ("Zaragoza", "Zaragoza",       41.6488, -0.8891, "50001"),
    ("Zaragoza", "Calatayud",      41.3555, -1.6435, "50300"),
]
# fmt: on

COMPANY_SUFFIXES = [
    "Instalaciones Térmicas",
    "Servicios del Hogar",
    "Climatización y Energía",
    "Mantenimiento Industrial",
    "Soluciones Energéticas",
    "Técnicos del Calor",
    "Ingeniería de Fluidos",
    "Calderas y Servicios",
    "Grupo Técnico",
    "Servicios Integrales",
]

SERVICES = [
    "Instalación y puesta en marcha de dispositivos MHD.",
    "Instalación, mantenimiento y revisión anual de calderas.",
    "Instalación profesional y asistencia técnica MHD.",
    "Servicio técnico de calderas y sistemas de calefacción.",
    "Instalación de dispositivos MHD Agua y MHD Gas.",
    "Mantenimiento preventivo y correctivo de calderas.",
    "Instalaciones de calefacción y agua caliente sanitaria.",
    "Servicio oficial de instalación y post-venta MHD.",
]

TYPES = [
    Distributor.CompanyType.INSTALLER,
    Distributor.CompanyType.INSTALLER,
    Distributor.CompanyType.INSTALLER,
    Distributor.CompanyType.DISTRIBUTOR,
    Distributor.CompanyType.SERVICE_CENTER,
]

FIRST_NAMES = ["Carlos", "Ana", "Miguel", "Laura", "José", "María", "Antonio", "Elena",
               "Francisco", "Isabel", "David", "Patricia", "Javier", "Carmen", "Sergio",
               "Lucía", "Raúl", "Marta", "Alberto", "Rosa"]
LAST_NAMES = ["García", "Martínez", "López", "Sánchez", "González", "Fernández",
              "Pérez", "Rodríguez", "Jiménez", "Ruiz", "Álvarez", "Torres",
              "Ramírez", "Flores", "Moreno", "Ramos", "Cruz", "Herrera", "Díaz", "Navarro"]


class Command(BaseCommand):
    help = "Seed 100 fake approved distributors across Spanish provinces."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing seeded fake distributors before inserting.",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        if options["clear"]:
            deleted, _ = User.objects.filter(username__startswith="distrib_fake_").delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} fake distributor users."))

        created = 0
        for idx in range(1, 101):
            loc = LOCATIONS[(idx - 1) % len(LOCATIONS)]
            province, city, lat, lon, postal_code = loc

            suffix_idx = (idx - 1) % len(COMPANY_SUFFIXES)
            company_name = f"{city} {COMPANY_SUFFIXES[suffix_idx]}"
            if idx > len(COMPANY_SUFFIXES):
                company_name = f"{company_name} {idx}"

            first = FIRST_NAMES[(idx - 1) % len(FIRST_NAMES)]
            last1 = LAST_NAMES[(idx - 1) % len(LAST_NAMES)]
            last2 = LAST_NAMES[idx % len(LAST_NAMES)]
            contact = f"{first} {last1} {last2}"

            cif = f"B{idx:08d}"
            username = f"distrib_fake_{idx:03d}"
            email_user = f"distribuidores.mhd.{idx:03d}@example.com"

            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={"email": email_user, "first_name": first, "last_name": f"{last1} {last2}"},
            )

            company_type = TYPES[(idx - 1) % len(TYPES)]
            services = SERVICES[(idx - 1) % len(SERVICES)]

            _, dist_created = Distributor.objects.update_or_create(
                cif=cif,
                defaults={
                    "user": user,
                    "company_name": company_name,
                    "contact_person": contact,
                    "email": email_user,
                    "phone": f"+34 6{idx:02d} {(idx * 37) % 1000:03d} {(idx * 13) % 1000:03d}",
                    "address": f"Calle Mayor {idx}, {postal_code} {city}",
                    "province": province,
                    "city": city,
                    "postal_code": postal_code,
                    "latitude": round(lat + (idx % 5) * 0.01, 6),
                    "longitude": round(lon + (idx % 5) * 0.01, 6),
                    "company_type": company_type,
                    "status": Distributor.Status.APPROVED,
                    "services_offered": services,
                },
            )
            if dist_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Done. {created} new distributors created (rest already existed)."))
