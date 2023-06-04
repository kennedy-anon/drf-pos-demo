from django.db import models

# # to be cleared
# class Product(models.Model):
#     product_id = models.AutoField(primary_key=True, unique=True)
#     product_name = models.TextField(unique=True, max_length=255)
#     quantity = models.IntegerField()
#     buying_price = models.DecimalField(max_digits=7, decimal_places=2)
#     min_selling_price = models.DecimalField(max_digits=7, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)


# for storing product details
class ProductDetail(models.Model):
    product_id = models.AutoField(primary_key=True, unique=True)
    product_name = models.CharField(unique=True, max_length=255)
    min_selling_price = models.DecimalField(max_digits=7, decimal_places=2)
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
    buying_price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


# for storing sales history
class Sales(models.Model):
    product_id = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    units = models.IntegerField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
