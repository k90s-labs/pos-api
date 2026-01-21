from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = [
            'id',
            'company_id',
            'name',
            'trading_name',
            'abn',
            'phone',
            'address',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'company_id', 'created_at', 'updated_at']
    
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                "[EXCEPTION_001] Company name is required."
            )
        return value.strip()