# Generated by Django 4.2.7 on 2024-04-15 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0022_alter_venddoclines_recid'),
    ]

    operations = [
        migrations.AddField(
            model_name='excludedproductlist',
            name='qty',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество'),
        ),
    ]