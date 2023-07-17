from django.db import models

# for storing product details
class ProductDetail(models.Model):
    product_id = models.AutoField(primary_key=True, unique=True)
    product_name = models.CharField(unique=True, max_length=255)
    min_selling_price = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# maintaining the stock level
class StockLevel(models.Model):
    product_id = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    available_units = models.IntegerField()
    min_units_alert = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


# for storing purchase history
class PurchaseHistory(models.Model):
    product_id = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    units = models.IntegerField()
    buying_price = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


# for storing invoices
class Invoices(models.Model):
    invoice_no = models.AutoField(primary_key=True, unique=True)
    customer_name = models.CharField(max_length=255)
    customer_contact_no = models.BigIntegerField(null=True)
    invoice_amount = models.DecimalField(max_digits=14, decimal_places=2)
    invoice_paid = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


# for storing sales history
class Sales(models.Model):
    product_id = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    units = models.IntegerField()
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    sale_type = models.CharField(max_length=255, default='cash')
    invoice_no = models.ForeignKey(Invoices, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


