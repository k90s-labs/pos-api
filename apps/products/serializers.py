from rest_framework import serializers
from .models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category_id",
            "name_en",
            "name_ko",
            "purchase_price",
            "sale_price",
            "is_weight_based",
            "weight_kg",
            "supplier",
            "is_stock_managed",
            "stock_quantity",
            "is_taxable",
            "barcode",
            "is_fixed_price",
            "nickname",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
