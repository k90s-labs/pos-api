from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from .models import Category
from .serializers import CategorySerializer


class ProductPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_destroy(self, instance: Category) -> None:
        # 1) 자식 카테고리 존재하면 삭제 불가
        if instance.children.exists():
            raise ValidationError({"[EXCEPTION_000]detail": "This category has child categories and cannot be deleted."})

        # 2) 어떤 상품이라도 이 카테고리를 사용 중이면 삭제 불가
        # Product 모델의 category FK의 reverse 접근
        if instance.products.exists():
            raise ValidationError({"[EXCEPTION_000]detail": "This category is used by products and cannot be deleted."})

        instance.delete()
