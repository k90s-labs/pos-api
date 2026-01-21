from django.db import models
import uuid


class Company(models.Model):
    
    id = models.AutoField(primary_key=True)
    
    company_id = models.CharField(
        max_length=100,
        unique=True,
        editable=False
    )
    
    name = models.CharField(max_length=200)
    
    trading_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    
    abn = models.CharField(
        max_length=11,
        blank=True,
        null=True
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    
    address = models.TextField(
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'company'
        ordering = ['-created_at']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    
    
    def save(self, *args, **kwargs):
        if not self.company_id or self.company_id == "":
            self.company_id = f"COMP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f"{self.name} ({self.company_id})"