# Generated by Django 4.2.1 on 2023-06-24 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_historicalvarparam_value_alter_varparam_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
    ]
