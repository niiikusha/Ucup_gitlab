# Generated by Django 4.2.7 on 2024-04-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0044_delete_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('entity_id', models.CharField(blank=True, null=True, verbose_name='Entity')),
                ('customer_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='vendor_id')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('urastic_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='UrasticName')),
                ('inn_kpp', models.CharField(blank=True, max_length=121, null=True, verbose_name='INN/KPP')),
                ('director_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='DirectorName')),
                ('urastic_adress', models.CharField(blank=True, max_length=250, null=True, verbose_name='UrasticAdress')),
                ('account', models.CharField(blank=True, max_length=100, null=True, verbose_name='Account')),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='BankName')),
                ('bank_bik', models.CharField(blank=True, max_length=50, null=True, verbose_name='BankBik')),
                ('corr_account', models.CharField(blank=True, max_length=100, null=True, verbose_name='CorrAccount')),
                ('dir_party', models.BigIntegerField(blank=True, null=True, verbose_name='DirParty')),
            ],
            options={
                'db_table': 'customer',
            },
        ),
    ]
