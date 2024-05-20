# Generated by Django 4.2.7 on 2024-05-20 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0050_officialcustomer_rename_base_kucustomer_pay_sum_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='includedservice',
            name='article_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='LAMA_ucup.article'),
        ),
        migrations.AddField(
            model_name='includedservice',
            name='service_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='LAMA_ucup.service'),
        ),
        migrations.AlterField(
            model_name='kucustomer',
            name='customer_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='LAMA_ucup.customer'),
        ),
        migrations.AlterField(
            model_name='kucustomer',
            name='pay_sum',
            field=models.FloatField(blank=True, null=True, verbose_name='pay_sum'),
        ),
        migrations.AlterField(
            model_name='kugraphcustomer',
            name='customer_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='LAMA_ucup.customer'),
        ),
    ]