from rest_framework import serializers
from django.db import IntegrityError

from members.utils import generate_member_id
from .models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "member_id",
            "name",
            "phone_number",
            "joined_at",
            "last_visited_at",
            "points",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "joined_at",
            "last_visited_at",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "member_id": {"required": False},
        }

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        member_id = validated_data.get("member_id")

        # If member_id is not provided, we expect a prefix from the request
        if not member_id:
            if request is None:
                raise serializers.ValidationError(
                    {"member_id": "Either member_id or prefix is required."}
                )

            prefix = request.data.get("prefix")
            if not prefix:
                raise serializers.ValidationError(
                    {"member_id": "Either member_id or prefix is required."}
                )

            validated_data["member_id"] = generate_member_id(prefix)

        # points will default to 0 if not provided (model default),
        # but we keep your explicit behavior:
        if "points" not in validated_data:
            validated_data["points"] = 0

        try:
            return super().create(validated_data)
        except IntegrityError:
            # In case generated member_id is duplicated (race condition)
            raise serializers.ValidationError(
                {"member_id": "Generated member_id already exists. Please try again."}
            )