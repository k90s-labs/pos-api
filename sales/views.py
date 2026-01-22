from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .models import Sale
from .serializers import SaleSerializer


class SalePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    pagination_class = SalePagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "id",
        "member__member_id",
        "member__name",
        "items__product_name_ko",
        "items__product_name_en",
        "items__barcode",
    ]
    ordering_fields = [
        "sold_at",
        "total_amount",
        "subtotal_amount",
    ]
    ordering = ["-sold_at"]

    def get_queryset(self):
        # ✅ JOIN search로 중복 row 방지
        return Sale.objects.all().order_by("-sold_at").distinct()
