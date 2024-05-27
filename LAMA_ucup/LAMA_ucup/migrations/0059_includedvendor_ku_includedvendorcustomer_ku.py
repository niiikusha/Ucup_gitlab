# Generated by Django 4.2.7 on 2024-05-27 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0058_includedvendorcustomer'),
    ]

    operations = [
        migrations.AddField(
            model_name='includedvendor',
            name='ku',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='LAMA_ucup.ku'),
        ),
        migrations.AddField(
            model_name='includedvendorcustomer',
            name='ku',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='LAMA_ucup.ku'),
        ),
    ]