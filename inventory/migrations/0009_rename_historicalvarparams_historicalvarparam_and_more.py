# Generated by Django 4.1.5 on 2023-03-25 18:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0008_alter_varparams_variant'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoricalVarParams',
            new_name='HistoricalVarParam',
        ),
        migrations.RenameModel(
            old_name='VarParams',
            new_name='VarParam',
        ),
        migrations.AlterModelOptions(
            name='historicalvarparam',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical var param', 'verbose_name_plural': 'historical var params'},
        ),
    ]
