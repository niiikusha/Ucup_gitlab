# Generated by Django 4.2.7 on 2024-04-04 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0011_remove_product_property_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ku',
            name='ku_type',
            field=models.CharField(blank=True, choices=[('Ретро-бонус', 'Ретро-бонус'), ('Услуга', 'Услуга')], null=True, verbose_name='Тип КУ'),
        ),
        migrations.AlterField(
            model_name='ku',
            name='pay_method',
            field=models.CharField(blank=True, choices=[('Взаимозачет', 'Взаимозачет'), ('Оплата', 'Оплата')], null=True, verbose_name='Способ оплаты'),
        ),
    ]