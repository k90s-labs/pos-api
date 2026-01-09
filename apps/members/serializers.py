from rest_framework import serializers
from .models import Member


class MemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = [
            'id',
            'member_id',
            'name',
            'phone_number',
            'joined_at',
            'last_visited_at',
            'points',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'joined_at',
            'last_visited_at',
            'created_at',
            'updated_at',
        ]