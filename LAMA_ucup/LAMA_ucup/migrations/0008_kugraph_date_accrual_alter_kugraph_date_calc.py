# Generated by Django 4.2.7 on 2024-03-28 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0007_alter_assortment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='kugraph',
            name='date_accrual',
            field=models.DateField(blank=True, null=True, verbose_name='Дата начисления'),
        ),
        migrations.AlterField(
            model_name='kugraph',
            name='date_calc',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date_calc'),
        ),
    ]