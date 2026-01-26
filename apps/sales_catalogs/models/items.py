from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampedModel


class SalesCatalogItem(TimeStampedModel):
    # 7 * 5 = 35칸
    GRID_COLS = 7
    GRID_ROWS = 5
    MAX_POSITION = GRID_COLS * GRID_ROWS - 1  # 34

    # DB에는 hex 대신 "키"만 저장 (0~9)
    class ColorKey(models.IntegerChoices):
        C0 = 0, "C0"
        C1 = 1, "C1"
        C2 = 2, "C2"
        C3 = 3, "C3"
        C4 = 4, "C4"
        C5 = 5, "C5"
        C6 = 6, "C6"
        C7 = 7, "C7"
        C8 = 8, "C8"
        C9 = 9, "C9"
        C10 = 10, "C10"

    sales_catalog = models.ForeignKey(
        "sales_catalogs.SalesCatalog",
        on_delete=models.CASCADE,
        related_name="items",
        null=False,
        blank=False,
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="sales_catalog_items",
        null=False,
        blank=False,
    )

    # 0~34 (프론트에서 row/col로 변환해도 됨)
    position = models.IntegerField(null=False, blank=False)

    # 사용자가 버튼 표시명을 지정하면 사용, 없으면 product.nickname을 사용(프론트든 백이든 가능)
    label = models.CharField(max_length=255, null=True, blank=True)

    # 버튼별 컬러 선택을 "저장"하려면 키 값은 필요함 (hex는 저장 X)
    color_key = models.IntegerField(
        choices=ColorKey.choices,
        default=ColorKey.C0,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "sales_catalog_items"
        ordering = ["sales_catalog", "position"]
        constraints = [
            models.UniqueConstraint(
                fields=["sales_catalog", "position"],
                name="uq_sales_catalog_items__catalog_position",
            )
        ]
        indexes = [
            models.Index(fields=["sales_catalog"]),
            models.Index(fields=["product"]),
        ]

    def clean(self):
        super().clean()
        if self.position < 0 or self.position > self.MAX_POSITION:
            raise ValidationError(f"[EXCEPTION_000]position은 0~{self.MAX_POSITION} 범위여야 합니다.")

    @property
    def display_name(self) -> str:
        # 프론트에서 해도 되지만, 백에서 제공해두면 항상 일관됨
        if self.label:
            return self.label
        # Product.nickname이 null일 수 있으니 fallback 하나 더
        if getattr(self.product, "nickname", None):
            return self.product.nickname
        return self.product.name_ko
