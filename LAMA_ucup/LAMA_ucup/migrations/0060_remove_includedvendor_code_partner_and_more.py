# Generated by Django 4.2.7 on 2024-05-27 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0059_includedvendor_ku_includedvendorcustomer_ku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='includedvendor',
            name='code_partner',
        ),
        migrations.RemoveField(
            model_name='includedvendorcustomer',
            name='code_partner',
        ),
    ]
