from rest_framework import serializers
from django.db import IntegrityError

from .models import ProductDetail, PurchaseHistory, Sales #Product


# serializing product details
class ProductDetailSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=255, min_length=1, allow_blank=False, trim_whitespace=True)
    min_selling_price = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True, required=False)

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
            raise serializers.ValidationError({'detail': "Duplicate entry. This item already exists.", 'product_name': validated_data['product_name']})


# serializing purchase history
class PurchaseHistorySerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductDetail.objects.all()) # should be a PK in ProductDetail
    units = serializers.IntegerField()
    buying_price = serializers.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        model = PurchaseHistory
        fields = [
            'product_id',
            'units',
            'buying_price',
            'created_at'
        ]


# serializing sale invoice
class InvoiceSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255, allow_blank=True)
    customer_contact_no = serializers.CharField(max_length=255, allow_blank=True)
    invoice_amount = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True)
    invoice_paid = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True)


# serializing sale product
class PosProductSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductDetail.objects.all()) # should be a PK in ProductDetail
    units = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)


# serailizing pos
class PosSerializer(serializers.Serializer):
    products = PosProductSerializer(many=True)
    sale_type = serializers.CharField(max_length=255)
    total_sales = serializers.DecimalField(max_digits=14, decimal_places=2)
    cash_received = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True)
    change = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True)
    invoice = InvoiceSerializer()

    class meta:
        model = Sales
        fields = [
            'products',
            'sale_type',
            'total_sales',
            'cash_received',
            'change',
            'invoice',
            'created_at'
        ]
