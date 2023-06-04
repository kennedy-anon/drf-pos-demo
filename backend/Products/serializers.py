from rest_framework import serializers
from django.db import IntegrityError

from .models import ProductDetail, StockLevel, PurchaseHistory, Sales #Product


# serializing product details
class ProductDetailSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=255, min_length=1, allow_blank=False, trim_whitespace=True)
    min_selling_price = serializers.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        model = ProductDetail
        fields = [
            'product_id',
            'product_name',
            'min_selling_price',
            'created_at'
        ]

    def create(self, validated_data):
        try:
            return ProductDetail.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Duplicate entry. This item already exists.")


# # serializes the products
# class ProductSerializer(serializers.Serializer):
#     product_name = serializers.CharField(max_length=255, min_length=1, allow_blank=False, trim_whitespace=True)
#     quantity = serializers.IntegerField()
#     buying_price = serializers.DecimalField(max_digits=7, decimal_places=2)
#     min_selling_price = serializers.DecimalField(max_digits=7, decimal_places=2)

#     class Meta:
#         model = Product
#         fields = [
#             'product_id',
#             'product_name',
#             'quantity',
#             'buying_price',
#             'min_selling_price',
#             'created_at'
#         ]

#     def create(self, validated_data):
#         try:
#             return Product.objects.create(**validated_data)
#         except IntegrityError:
#             raise serializers.ValidationError("Duplicate entry. This item already exists.")
