# Generated by Django 4.2.1 on 2023-06-07 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_historicalvarparam_value_alter_varparam_value'),
        ('order', '0004_alter_cart_variants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='variants',
            field=models.ManyToManyField(blank=True, related_name='carts', through='order.CartItem', to='inventory.variant'),
        ),
    ]
