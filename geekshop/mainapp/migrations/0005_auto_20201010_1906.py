# Generated by Django 3.1.2 on 2020-10-10 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20201010_1846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_acitve',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='productcategory',
            old_name='is_acitve',
            new_name='is_active',
        ),
    ]
