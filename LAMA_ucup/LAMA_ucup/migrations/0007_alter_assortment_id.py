# Generated by Django 4.2.7 on 2024-03-28 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0006_alter_assortment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assortment',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
