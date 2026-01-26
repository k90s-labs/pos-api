from django.db import models

class TimeStampedModel(models.Model):
    """
    created_at / updated_at 자동 관리용 추상 모델
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True