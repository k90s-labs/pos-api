from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            "id",
            "supplier_name",
            "abn",
            "contact",
            "mobile",
            "email",
            "address1",
            "address2",
            "suburb",
            "state",
            "postcode",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
