import json
import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
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

    basket = Basket.objects.filter(user=request.user)

    if category_pk is not None:
        if category_pk == "0":
            product_items = Product.objects.all()
            category = {
                'name': 'все'
            }
        else:
            category = get_object_or_404(ProductCategory, pk=category_pk)
            product_items = Product.objects.filter(category=category)

        content = {
            'contact_links': contact_links,
            'menu_links': menu_links,
            'category': category,
            'products': product_items,
            'basket': basket
        }
        return render(request, "mainapp/products_list.html", content)

    prods = Product.objects.all()[:3]
    content = {
        'contact_links': contact_links,
        'menu_links': menu_links,
        'products': prods,
        'basket': basket
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    contacts = Contacts.objects.all()
    content = {
        'contact_links': contact_links,
        'products': products,
        'contacts': contacts
    }

    return render(request, 'mainapp/contact.html', content)
