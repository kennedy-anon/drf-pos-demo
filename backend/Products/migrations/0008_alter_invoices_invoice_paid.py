# Generated by Django 4.1.9 on 2023-07-17 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0007_alter_invoices_customer_contact_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='invoice_paid',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
    ]