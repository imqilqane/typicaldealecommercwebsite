# Generated by Django 3.0 on 2020-05-14 23:34

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_auto_20200514_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='descount_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='descraption',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
