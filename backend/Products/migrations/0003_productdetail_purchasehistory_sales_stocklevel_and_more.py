# Generated by Django 4.1.9 on 2023-06-04 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_alter_product_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('product_name', models.CharField(max_length=255, unique=True)),
                ('min_selling_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.IntegerField()),
                ('buying_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productdetail')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productdetail')),
            ],
        ),
        migrations.CreateModel(
            name='StockLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_units', models.IntegerField()),
                ('min_units_alert', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productdetail')),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]