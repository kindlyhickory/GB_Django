import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, Contacts

FILE_PATH = os.path.join(settings.BASE_DIR, 'mainapp\\json')


def load_from_json(file_name):
    with open(os.path.join(FILE_PATH, file_name + ".json"), encoding="utf-8") as json_file:
        return json.load(json_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json("categories")
        ProductCategory.objects.all().delete()
        for cat in categories:
            ProductCategory.objects.create(**cat)

        products = load_from_json("products")

        for prod in products:
            cat_name = prod['category']
            _cat = ProductCategory.objects.get(name=cat_name)
            prod['category'] = _cat
            Product.objects.create(**prod)

        contact_locations = load_from_json("contact__locations")
        Contacts.objects.all().delete()

        for cont in contact_locations:
            Contacts.objects.create(**cont)

        ShopUser.objects.create_superuser(username='django', password='geekbrains', age='30')
