# Generated by Django 4.2.7 on 2024-04-28 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0035_placeservice_alter_article_article_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeservice',
            name='address',
            field=models.CharField(blank=True, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterModelTable(
            name='placeservice',
            table='place_service',
        ),
    ]
