import json
import os

from django.conf import settings
from django.shortcuts import render

from mainapp.models import Product

from mainapp.models import Contacts

from mainapp.models import ProductCategory

contact_links = [
    {'href': 'contacts_facebook', 'name': 'social1'},
    {'href': 'contacts_twitter', 'name': 'social2'},
    {'href': 'contacts_google_plus', 'name': 'social3'},
    {'href': 'contacts_pinterest', 'name': 'social4'}
]


def main(request):
    prods = Product.objects.all()[:3]
    content = {
        'contact_links': contact_links,
        'products': prods,
    }
    return render(request, 'mainapp/index.html', content)


# Create your views here.

def products(request, category_pk=None):
    menu_links = ProductCategory.objects.all()
    prods = Product.objects.all()[:3]

    content = {
        'contact_links': contact_links,
        'menu_links': menu_links,
        'products': prods,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    contacts = Contacts.objects.all()
    content = {
        'contact_links': contact_links,
        'products': products,
        'contacts': contacts
    }
    # with open(os.path.join(settings.BASE_DIR,'contacts.json'), encoding="utf-8") as json_contacts:
    #     json_data = json_contacts.read()
    #     locations = json.loads(json_data)
    #     for i in range(len(locations)):
    #         Contacts.objects.create(city=locations[i]['city'],
    #                                 email=locations[i]['email'],
    #                                 phone_number=locations[i]['phone_number'],
    #                                 post_address=locations[i]['post_address'])

    return render(request, 'mainapp/contact.html', content)
