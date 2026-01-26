# suppliers/catalogs.py
from django.db import models
from core.models import TimeStampedModel


class Supplier(TimeStampedModel):
    supplier_name = models.CharField(max_length=255, null=False, blank=False)

    abn = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        unique=True,
    )

    contact = models.CharField(max_length=255, null=False, blank=False)

    mobile = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    suburb = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)

    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "suppliers"
        indexes = [
            models.Index(fields=["abn"]),
            models.Index(fields=["supplier_name"]),
        ]

    def __str__(self):
        return f"{self.supplier_name} ({self.abn})"
