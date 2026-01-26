from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from .models import Supplier
from .serializers import SupplierSerializer

class ProductPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by("-id")
    serializer_class = SupplierSerializer

    def perform_destroy(self, instance: Supplier) -> None:
        # Product.supplier에 related_name="products" 이므로 Supplier 역참조는 instance.products
        if instance.products.exists():
            raise ValidationError(
                {"detail": "This supplier is used by products and cannot be deleted."}
            )
        instance.delete()
