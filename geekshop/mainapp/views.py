import json
import os
import random

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


def get_basket(user):
    basket = []
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    product_list = Product.objects.all()
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category_id=hot_product.category_id).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    prods = Product.objects.all()[:3]
    content = {
        'contact_links': contact_links,
        'products': prods,
        'basket': get_basket(request.user)
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
            'basket': get_basket(request.user)
        }
        return render(request, "mainapp/products_list.html", content)

    prods = Product.objects.all()[:3]
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    content = {
        'contact_links': contact_links,
        'menu_links': menu_links,
        'products': prods,
        'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    contacts = Contacts.objects.all()
    content = {
        'contact_links': contact_links,
        'products': products,
        'contacts': contacts,
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/contact.html', content)


def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    title = product_item.name
    content = {
        'product': product_item,
        'basket': get_basket(request.user),
        'menu_links': ProductCategory.objects.all(),
        'title': title,
        'same_products': get_same_products(product_item)
    }

    return render(request, 'mainapp/product.html', content)
