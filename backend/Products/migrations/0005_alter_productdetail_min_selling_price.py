# Generated by Django 4.1.9 on 2023-07-09 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_alter_productdetail_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='min_selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
