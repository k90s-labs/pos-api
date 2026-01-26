from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.members.models import Member
from apps.products.models import Product
from core.models import TimeStampedModel


class Sale(TimeStampedModel):
    member = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales",
    )

    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ("OTHER", "Other"),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default="CASH")

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("CANCELLED", "Cancelled"),
        ("REFUNDED", "Refunded"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PAID")

    sold_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "sales"
        indexes = [
            models.Index(fields=["sold_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["member"]),
        ]

    def __str__(self):
        return f"Sale #{self.id} - {self.total_amount}"

    def clean(self):
        super().clean()
        if self.discount_amount < 0:
            raise ValidationError("[EXCEPTION_000]discount_amount must be greater than or equal to 0.")
        if self.total_amount < 0:
            raise ValidationError("[EXCEPTION_000]total_amount must be greater than or equal to 0.")


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_items",
    )

    # Snapshot fields
    product_name_en = models.CharField(max_length=255)
    product_name_ko = models.CharField(max_length=255)
    barcode = models.CharField(max_length=64)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField(default=1)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    line_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "sale_items"
        indexes = [
            models.Index(fields=["sale"]),
            models.Index(fields=["product"]),
            models.Index(fields=["barcode"]),
        ]

    def __str__(self):
        return f"{self.product_name_ko} x {self.quantity or self.weight_kg}"

    def clean(self):
        super().clean()

        if not self.product_id:
            raise ValidationError("[EXCEPTION_000]product is required for a sale item.")

        if self.product.is_weight_based:
            if self.weight_kg is None or self.weight_kg <= 0:
                raise ValidationError("[EXCEPTION_000]weight_kg must be greater than 0 for weight-based products.")
            if self.quantity <= 0:
                raise ValidationError("[EXCEPTION_000]quantity must be at least 1 for weight-based products.")
        else:
            if self.quantity <= 0:
                raise ValidationError("[EXCEPTION_000]quantity must be greater than 0 for non weight-based products.")
            if self.weight_kg is not None:
                raise ValidationError("[EXCEPTION_000]weight_kg must be empty for non weight-based products.")
