# Generated by Django 4.2.7 on 2024-03-28 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0003_alter_bonuscondition_criterion'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='property_1',
            field=models.CharField(blank=True, null=True, verbose_name='Property 1'),
        ),
    ]
