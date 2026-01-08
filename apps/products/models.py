from django.db import models


class Product(models.Model):
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

    # Weight-based pricing
    is_weight_based = models.BooleanField(null=False)
    weight_kg = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True
    )

    # Supplier
    supplier = models.CharField(max_length=255, null=False, blank=False)

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

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
