# Generated by Django 4.2.7 on 2024-04-11 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0021_alter_venddoclines_recid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venddoclines',
            name='recid',
            field=models.BigAutoField(default=2567072, primary_key=True, serialize=False, verbose_name='RecId'),
        ),
    ]
