# Generated by Django 4.2.7 on 2024-04-15 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0026_alter_excludedproductlist_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excludedproductlist',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
