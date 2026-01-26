from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from core.models import TimeStampedModel

class Product(TimeStampedModel):
    # Category
    category = models.ForeignKey(
        "categories.Category",     # app_label.ModelName
        on_delete=models.PROTECT,
        related_name="products",
        null=False,
        blank=False,
    )


    # Names
    name_en = models.CharField(max_length=255, null=False, blank=False)
    name_ko = models.CharField(max_length=255, null=False, blank=False)

    # Pricing
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )

    # Discount information
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_start_at = models.DateTimeField(null=True, blank=True)
    discount_end_at = models.DateTimeField(null=True, blank=True)

    # Weight-based pricing
    is_weight_based = models.BooleanField(null=False)
    weight_kg = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True
    )

    # Supplier
    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.PROTECT,
        related_name="products",
        null=False,
        blank=False,
    )

    # Stock
    is_stock_managed = models.BooleanField(null=False)
    stock_quantity = models.IntegerField(null=True, blank=True)

    # Tax
    is_taxable = models.BooleanField(null=False)

    # Barcode
    barcode = models.CharField(
        max_length=64, null=False, blank=False
    )

    # Pricing type
    is_fixed_price = models.BooleanField(null=False)

    # Optional
    nickname = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "products"
        indexes = [
            models.Index(fields=["barcode"]),
            models.Index(fields=["name_en"]),
            models.Index(fields=["name_ko"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.name_en} ({self.barcode})"

    # 정합성 체크: 일부만 채워지는 상황 방지 + 기간/가격 검증
    def clean(self):
        super().clean()

        fields = [self.discount_price, self.discount_start_at, self.discount_end_at]
        filled = [v is not None for v in fields]

        # 3개 중 하나라도 채우면 3개가 모두 있어야 함
        if any(filled) and not all(filled):
            raise ValidationError(
                "[EXCEPTION_000]discount_price, discount_start_at, discount_end_at은 함께 설정되어야 합니다."
            )

        if self.discount_start_at and self.discount_end_at:
            if self.discount_end_at <= self.discount_start_at:
                raise ValidationError("[EXCEPTION_000]discount_end_at은 discount_start_at 이후여야 합니다.")

        if self.discount_price is not None:
            if self.discount_price <= 0:
                raise ValidationError("[EXCEPTION_000]discount_price는 0보다 커야 합니다.")
            # 정책: 할인가가 정가보다 크거나 같으면 할인 의미가 없으니 막기 (원하면 제거 가능)
            if self.discount_price >= self.sale_price:
                raise ValidationError("[EXCEPTION_000]discount_price는 sale_price보다 작아야 합니다.")

    @property
    def is_discount_active(self) -> bool:
        if not (self.discount_price and self.discount_start_at and self.discount_end_at):
            return False
        now = timezone.now()
        return self.discount_start_at <= now < self.discount_end_at

    @property
    def current_price(self):
        return self.discount_price if self.is_discount_active else self.sale_price
