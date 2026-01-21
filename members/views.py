from django.db import transaction
from django.db.models import F
from django.utils import timezone

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Member
from .serializers import MemberSerializer
from .utils import generate_member_id


class MemberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class MemberViewSet(viewsets.ModelViewSet):
    """
    Member CRUD + 검색 + 정렬 + 포인트 관련 커스텀 액션
    """

    queryset = Member.objects.all().order_by("-joined_at")
    serializer_class = MemberSerializer
    pagination_class = MemberPagination

    # permission_classes = [permissions.IsAuthenticated]  # 나중에 권한 붙이면 사용

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["member_id", "name", "phone_number"]
    ordering_fields = ["joined_at", "last_visited_at", "points"]
    ordering = ["-joined_at"]

    @action(detail=False, methods=["get"], url_path="generate-id")
    def generate_id(self, request):
        """
        GET /members/generate-id/?prefix=ABC
        → { "member_id": "ABC00001" }
        """
        prefix = request.query_params.get("prefix")
        if not prefix:
            return Response(
                {
                    "detail": (
                        "[EXCEPTION_000] The 'prefix' query parameter is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            member_id = generate_member_id(prefix)
        except ValueError as e:
            return Response(
                {
                    "detail": (
                        f"[EXCEPTION_000] {str(e)}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"member_id": member_id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="add-points")
    def add_points(self, request, pk=None):
        """
        POST /members/{id}/add-points/
        Body: { "points": 100 }

        → 포인트 적립 + last_visited_at 갱신
        """
        member = self.get_object()

        raw_points = request.data.get("points", 0)
        try:
            points = int(raw_points)
        except (TypeError, ValueError):
            return Response(
                {
                    "detail": (
                        "[EXCEPTION_000] points must be an integer."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if points <= 0:
            return Response(
                {
                    "detail": (
                        "[EXCEPTION_000] points must be a positive integer."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        Member.objects.filter(pk=member.pk).update(
            points=F("points") + points,
            last_visited_at=timezone.now(),
        )

        member.refresh_from_db()
        serializer = self.get_serializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="use-points")
    def use_points(self, request, pk=None):
        """
        POST /members/{id}/use-points/
        Body: { "points": 1000 }

        → 포인트 사용 (차감) + last_visited_at 갱신
        """
        member = self.get_object()

        raw_points = request.data.get("points", 0)
        try:
            amount = int(raw_points)
        except (TypeError, ValueError):
            return Response(
                {
                    "detail": (
                        "[EXCEPTION_000] points must be an integer."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount <= 0:
            return Response(
                {
                    "detail": (
                        "[EXCEPTION_000] points must be a positive integer."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            updated = (
                Member.objects
                .filter(pk=member.pk, points__gte=amount)
                .update(
                    points=F("points") - amount,
                    last_visited_at=timezone.now(),
                )
            )

            if updated == 0:
                return Response(
                    {
                        "detail": (
                            "[EXCEPTION_000] Not enough points."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        member.refresh_from_db()
        serializer = self.get_serializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)
