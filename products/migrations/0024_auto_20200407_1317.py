# Generated by Django 3.0 on 2020-04-07 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20200407_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Shipping_adress',
        ),
        migrations.AlterField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
