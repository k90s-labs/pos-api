from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(source="parent.id", read_only=True)
    children_count = serializers.IntegerField(source="children.count", read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name_en",
            "name_ko",
            "parent",       # 쓰기용 (id로 입력)
            "parent_id",    # 읽기용
            "children_count", # children_count는 삭제 검증할 때 UI에도 도움 됨
            "is_active",
            "sort_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "parent_id", "children_count"]
