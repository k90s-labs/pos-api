from django.db import models
from core.models import TimeStampedModel


class SalesCatalog(TimeStampedModel):
    name = models.CharField(max_length=10, null=False, blank=False)
    sort_order = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "sales_catalogs"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return self.name
