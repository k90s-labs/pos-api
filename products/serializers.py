from rest_framework import serializers
from .models import Product

# Product 모델 → JSON 응답 형태로 “변환”하는 규칙 정의
# DB 모델을 그대로 노출 x
# API 응답에 어떤 필드를, 어떤 형태로 보여줄지 결정

class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    supplier_id = serializers.IntegerField(source="supplier.id", read_only=True)

    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_discount_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",      # 입력: category id
            "category_id",   # 출력 편의
            "supplier",      # 입력: supplier id
            "supplier_id",   # 출력 편의

            "name_en",
            "name_ko",
            "purchase_price",
            "sale_price",

            "is_discount_active",
            "discount_price",
            "discount_start_at",
            "discount_end_at",
            "current_price",

            "is_weight_based",
            "weight_kg",

            "is_stock_managed",
            "stock_quantity",

            "is_taxable",
            "barcode",
            "is_fixed_price",
            "nickname",

            "created_at",
            "updated_at",

            # "current_price",
            # "is_discount_active",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]