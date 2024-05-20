# Generated by Django 4.2.7 on 2024-04-02 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMA_ucup', '0009_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand_name',
            field=models.CharField(blank=True, null=True, verbose_name='Property 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_name',
            field=models.CharField(blank=True, null=True, verbose_name='Property 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='external_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Внешний id'),
        ),
        migrations.AddField(
            model_name='product',
            name='group_category_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Внешний id'),
        ),
        migrations.AddField(
            model_name='product',
            name='price_segment',
            field=models.CharField(blank=True, null=True, verbose_name='Property 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_group_category_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Внешний id'),
        ),
        migrations.AlterField(
            model_name='bonuscondition',
            name='criterion',
            field=models.FloatField(blank=True, default=0.0),
        ),
    ]