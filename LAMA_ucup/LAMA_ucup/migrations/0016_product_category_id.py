# Generated by Django 4.2.7 on 2024-04-09 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0015_alter_product_brand_name_alter_product_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='ключ категории'),
        ),
    ]