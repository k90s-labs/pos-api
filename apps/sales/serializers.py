from decimal import Decimal

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Sale, SaleItem
from apps.products.models import Product


class SaleItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "product",
            "product_name_en",
            "product_name_ko",
            "barcode",
            "unit_price",
            "quantity",
            "weight_kg",
            "line_total",
        ]
        read_only_fields = [
            "id",
            "product_name_en",
            "product_name_ko",
            "barcode",
            "unit_price",
            "line_total",
        ]

    def validate(self, attrs):
        product: Product = attrs.get("product")
        quantity = attrs.get("quantity")
        weight_kg = attrs.get("weight_kg")

        if not product:
            raise serializers.ValidationError({"product": "[EXCEPTION_000]product is required."})

        if product.is_weight_based:
            if weight_kg is None or weight_kg <= 0:
                raise serializers.ValidationError(
                    {"weight_kg": "[EXCEPTION_000]weight_kg must be greater than 0 for weight-based products."}
                )
            if quantity is None or quantity <= 0:
                raise serializers.ValidationError(
                    {"quantity": "[EXCEPTION_000]quantity must be at least 1 for weight-based products."}
                )
        else:
            if quantity is None or quantity <= 0:
                raise serializers.ValidationError(
                    {"quantity": "[EXCEPTION_000]quantity must be greater than 0 for non weight-based products."}
                )
            if weight_kg is not None:
                raise serializers.ValidationError(
                    {"weight_kg": "[EXCEPTION_000]weight_kg must be empty for non weight-based products."}
                )

        return attrs


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, required=False)

    class Meta:
        model = Sale
        fields = [
            "id",
            "member",
            "subtotal_amount",
            "discount_amount",
            "total_amount",
            "payment_method",
            "status",
            "sold_at",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "subtotal_amount",
            "total_amount",
            "created_at",
            "updated_at",
        ]

    def validate_discount_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("[EXCEPTION_000]discount_amount must be greater than or equal to 0.")
        return value

    def validate(self, attrs):
        # items required only on create
        if self.instance is None:
            items = self.initial_data.get("items")
            if not items:
                raise serializers.ValidationError({"items": "[EXCEPTION_000]at least one item is required."})
        return attrs

    def _prepare_items_and_totals(self, items_data, discount_amount: Decimal):
        subtotal = Decimal("0")

        for item in items_data:
            product: Product = item["product"]

            item["product_name_en"] = product.name_en
            item["product_name_ko"] = product.name_ko
            item["barcode"] = product.barcode

            unit_price = Decimal(str(product.current_price))
            item["unit_price"] = unit_price

            if product.is_weight_based:
                weight_kg = item.get("weight_kg")
                line_total = unit_price * Decimal(str(weight_kg))
            else:
                quantity = item.get("quantity", 1)
                line_total = unit_price * quantity

            item["line_total"] = line_total
            subtotal += line_total

        total = subtotal - discount_amount
        if total < 0:
            raise serializers.ValidationError(
                {"discount_amount": "[EXCEPTION_000]discount_amount cannot be greater than subtotal_amount."}
            )

        return items_data, subtotal, total

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        discount_amount = validated_data.get("discount_amount") or Decimal("0")

        items_data, subtotal, total = self._prepare_items_and_totals(
            items_data, Decimal(str(discount_amount))
        )
        validated_data["subtotal_amount"] = subtotal
        validated_data["total_amount"] = total

        sale = Sale.objects.create(**validated_data)

        for item_data in items_data:
            try:
                SaleItem.objects.create(sale=sale, **item_data)
            except DjangoValidationError as e:
                raise serializers.ValidationError({"items": f"[EXCEPTION_000]{e.messages[0]}"})

        return sale

    def update(self, instance, validated_data):
        """
        - If items provided: rebuild items + recompute subtotal/total
        - If items NOT provided: still recompute total if discount_amount changed
        """
        items_data = validated_data.pop("items", None)

        discount_before = instance.discount_amount
        subtotal_before = instance.subtotal_amount

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if items_data is not None:
            if not items_data:
                raise serializers.ValidationError({"items": "[EXCEPTION_000]at least one item is required."})

            instance.items.all().delete()

            discount_amount = instance.discount_amount or Decimal("0")
            items_data, subtotal, total = self._prepare_items_and_totals(
                items_data, Decimal(str(discount_amount))
            )
            instance.subtotal_amount = subtotal
            instance.total_amount = total

            for item_data in items_data:
                try:
                    SaleItem.objects.create(sale=instance, **item_data)
                except DjangoValidationError as e:
                    raise serializers.ValidationError({"items": f"[EXCEPTION_000]{e.messages[0]}"})
        else:
            # ✅ items 없이 discount만 바꾸는 PATCH에서도 total이 맞도록
            if instance.discount_amount != discount_before:
                total = Decimal(str(subtotal_before)) - Decimal(str(instance.discount_amount or 0))
                if total < 0:
                    raise serializers.ValidationError(
                        {"discount_amount": "[EXCEPTION_000]discount_amount cannot be greater than subtotal_amount."}
                    )
                instance.total_amount = total

        instance.save()
        return instance
