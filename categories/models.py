from django.db import models


class Category(models.Model):
    name_en = models.CharField(max_length=255, null=False, blank=False)
    name_ko = models.CharField(max_length=255, null=False, blank=False)

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )

    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        ordering = ["sort_order", "name_en"]

    def __str__(self) -> str:
        return self.name_en
