# Generated by Django 4.2.7 on 2024-03-26 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0002_alter_excludedvenddoc_doc_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonuscondition',
            name='criterion',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
