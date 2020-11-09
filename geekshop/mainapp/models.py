from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='имя')
    description = models.TextField(blank=True, verbose_name='описание')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='имя')
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(max_length=128, verbose_name='короткое описание')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class Contacts(models.Model):
    city = models.CharField(max_length=20, verbose_name='город')
    phone_number = models.CharField(max_length=15, verbose_name='телефон')
    email = models.CharField(max_length=40, verbose_name='электронная почта')
    post_address = models.CharField(max_length=128, verbose_name='почтовый адрес')

    def __str__(self):
        return f'{self.email} ({self.phone_number})'
