from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class ProductPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 50

class ProductViewSet(viewsets.ModelViewSet):
    queryset = (
        Product.objects
        .select_related("category", "supplier")
        .all()
        .order_by("-id")
    )
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    # 필터/검색/정렬
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # 카테고리/서플라이어 "필터" (id 기반)
    filterset_fields = ["category", "supplier"]

    # 통합 검색 (사용자는 ?search= 로만)
    # - name_en, name_ko: 상품명 통합
    # - barcode: 바코드
    # - nickname: 닉네임
    search_fields = ["name_en", "name_ko", "barcode", "nickname"]

    # (선택) 정렬 허용 필드
    ordering_fields = ["id", "name_en", "name_ko", "sale_price", "created_at", "updated_at"]
    ordering = ["-id"]
