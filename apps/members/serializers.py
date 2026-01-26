from django.db import IntegrityError
from rest_framework import serializers

from .models import Member
from .utils import generate_member_id


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
            "points",      # 생성 시 0으로 시작, 업데이트는 View 쪽에서
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "member_id": {"required": False},
        }

    def validate_phone_number(self, value):
        """
        전화번호 검증:
        - 현재는 숫자만 허용
        - 나중에 포맷 강화 가능
        """
        if not value.isdigit():
            raise serializers.ValidationError(
                "[EXCEPTION_000] Phone number must contain only digits."
            )
        return value

    def create(self, validated_data):
        """
        멤버 생성 로직:
        - member_id가 직접 들어오면 그대로 사용
        - 없으면 request.data.prefix 로 generate_member_id 호출
        - 포인트는 항상 0으로 시작
        """
        request = self.context.get("request")

        member_id = validated_data.get("member_id")
        if not member_id:
            # 요청 컨텍스트가 없는 경우
            if request is None:
                raise serializers.ValidationError(
                    {
                        "member_id": (
                            "[EXCEPTION_000] member_id or prefix is required."
                        )
                    }
                )

            prefix = request.data.get("prefix")
            if not prefix:
                raise serializers.ValidationError(
                    {
                        "member_id": (
                            "[EXCEPTION_000] member_id or prefix is required."
                        )
                    }
                )

            validated_data["member_id"] = generate_member_id(prefix)

        # 포인트는 항상 0으로 시작 (추가로 들어온 값이 있으면 유지)
        validated_data.setdefault("points", 0)

        try:
            return super().create(validated_data)
        except IntegrityError:
            # unique 제약으로 인한 중복 ID 발생 시 (race condition 등)
            raise serializers.ValidationError(
                {
                    "member_id": (
                        "[EXCEPTION_000] This member_id already exists. "
                        "Please try again."
                    )
                }
            )
