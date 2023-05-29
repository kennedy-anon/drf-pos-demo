from django.db import models

# for storing products
class Product(models.Model):
    product_id = models.AutoField(primary_key=True, unique=True)
    product_name = models.TextField(unique=True, max_length=255)
    quantity = models.IntegerField()
    buying_price = models.DecimalField(max_digits=7, decimal_places=2)
    min_selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
