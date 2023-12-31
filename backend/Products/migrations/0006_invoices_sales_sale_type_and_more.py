# Generated by Django 4.1.9 on 2023-07-17 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_alter_productdetail_min_selling_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('invoice_no', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_contact_no', models.BigIntegerField(null=True)),
                ('invoice_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('invoice_paid', models.DecimalField(decimal_places=2, max_digits=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='sales',
            name='sale_type',
            field=models.CharField(default='cash', max_length=255),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='min_selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='purchasehistory',
            name='buying_price',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
        migrations.AlterField(
            model_name='sales',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
        migrations.AddField(
            model_name='sales',
            name='invoice_no',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Products.invoices'),
        ),
    ]
