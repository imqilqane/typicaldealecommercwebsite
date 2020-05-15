# Generated by Django 3.0 on 2020-04-05 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20200405_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='active',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]