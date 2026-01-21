from django.db import models
from django.utils import timezone


class Member(models.Model):

    # Default Info
    name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)

    # Member ID (prefix + number)
    member_id = models.CharField(max_length=50, unique=True, null=False, blank=False)

    # Dates
    joined_at = models.DateTimeField(default=timezone.now, null=False, blank=False)
    last_visited_at = models.DateTimeField(null=True, blank=True)

    # Points (1000pt = $1)
    points = models.IntegerField(default=0, null=False, blank=False)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members"
        indexes = [
            models.Index(fields=["member_id"]),
            models.Index(fields=["phone_number"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.member_id})"
