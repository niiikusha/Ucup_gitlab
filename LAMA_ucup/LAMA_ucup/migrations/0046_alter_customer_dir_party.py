# Generated by Django 4.2.7 on 2024-04-28 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0045_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='dir_party',
            field=models.CharField(blank=True, null=True, verbose_name='DirParty'),
        ),
    ]