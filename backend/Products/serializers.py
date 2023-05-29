from rest_framework import serializers

from .models import Product

# serializes the products
class ProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=255, min_length=1, allow_blank=False, trim_whitespace=True)
    quantity = serializers.IntegerField()
    buying_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    min_selling_price = serializers.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        model = Product
        fields = [
            'product_id',
            'product_name',
            'quantity',
            'buying_price',
            'min_selling_price',
            'created_at'
        ]