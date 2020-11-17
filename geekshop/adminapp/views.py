from django.contrib.auth.decorators import user_passes_test
from django.contrib.sessions.backends import db
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from ordersapp.models import Order


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Пользователи'
        return context_data


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание пользователя'
        return context_data


class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование пользователя'
        return context_data


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoriesCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание категории'
        return context_data


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Категории'
        return context_data


class CategoriesUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование категории'
        return context_data

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'Применяется скидка {discount}% к товарной категории {self.object.name}')
                self.object.product_set.update(price=F('price')*(1-discount/100))
        return super().form_valid(form)


class CategoriesDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Категории'
        context_data['pk'] = self.request.resolver_match.kwargs['pk']
        return context_data

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(category_id=self.request.resolver_match.kwargs['pk'])


class ProductsCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание продукта'
        context_data['pk'] = self.request.resolver_match.kwargs['pk']
        return context_data


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Продукт'
        context_data['obj'] = Product.objects.filter(pk=self.request.resolver_match.kwargs['pk'])
        context_data['pk'] = self.request.resolver_match.kwargs['pk']
        return context_data


class ProductsEditView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование продукта'
        context_data['pk'] = self.request.resolver_match.kwargs['pk']
        return context_data

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.object.category_id])


class ProductsDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.object.category_id])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление продукта'
        context_data['pk'] = self.request.resolver_match.kwargs['pk']
        return context_data

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class OrdersListView(ListView):
    model = Order
    template_name = 'adminapp/orders_read.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['statuses'] = {
            'FM': 'формируется',
            'STP': 'отправлен в обработку',
            'PD': 'оплачен',
            'PRD': 'обрабатывается',
            'RDY': 'готов к выдаче',
        }
        return context_data


def order_change_status(request, status, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = status
    order.save()

    return HttpResponseRedirect(reverse('admin:orders_read'))


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender,instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
