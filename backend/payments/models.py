from django.db import models

from Products.models import Invoices

# for credit sales payments
class CreditSalePayment(models.Model):
    payment_id = models.AutoField(primary_key=True, unique=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    invoice_no = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
