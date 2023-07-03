# Registering models to be indexed in algolia search

from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import ProductDetail

@register(ProductDetail)
class ProductDetailIndex(AlgoliaIndex):
    fields = ('product_id', 'product_name', 'min_selling_price')
    settings = {'searchableAttributes': ['product_name']}
    index_name = 'dev_DenloyPOS'

