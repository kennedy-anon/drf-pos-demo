from rest_framework import generics

from .models import CreditSalePayment
from api.permissions import IsAdminPermission
from .serializers import CreditSalePaymentSerializer

# for credit sale payments
class CreditSalePaymentCreateAPIView(generics.CreateAPIView):
    queryset = CreditSalePayment.objects.all()
    serializer_class = CreditSalePaymentSerializer
    permission_classes = [IsAdminPermission]