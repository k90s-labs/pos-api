from django.utils import timezone
from django.db.models import F
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Member
from .serializers import MemberSerializer
from .utils import generate_member_id


class MemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing members (CRUD, search, ordering, custom actions).
    """

    queryset = Member.objects.all().order_by("-joined_at")
    serializer_class = MemberSerializer

    # Optional: restrict to logged-in users
    # permission_classes = [permissions.IsAuthenticated]

    # Enable search and sorting in the API
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["member_id", "name", "phone_number"]
    ordering_fields = ["joined_at", "last_visited_at", "points"]
    ordering = ["-joined_at"]

    @action(detail=False, methods=["get"], url_path="generate-id")
    def generate_id(self, request):
        """
        GET /members/generate-id/?prefix=ABC
        Returns a new member_id based on the given prefix.
        """
        prefix = request.query_params.get("prefix")
        if not prefix:
            return Response(
                {"detail": "The 'prefix' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            member_id = generate_member_id(prefix)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"member_id": member_id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="add-points")
    def add_points(self, request, pk=None):
        """
        POST /members/{id}/add-points/
        Body: { "points": 100 }

        Increases the member's points and updates last_visited_at.
        """
        member = self.get_object()

        # Validate points value
        raw_points = request.data.get("points", 0)

        try:
            points = int(raw_points)
        except (TypeError, ValueError):
            return Response(
                {"detail": "points must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if points <= 0:
            return Response(
                {"detail": "points must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Atomic update: points and last_visited_at in one query
        Member.objects.filter(pk=member.pk).update(
            points=F("points") + points,
            last_visited_at=timezone.now(),
        )

        # Refresh the instance from DB so serializer has latest values
        member.refresh_from_db()

        serializer = self.get_serializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)
    queryset = Member.objects.all().order_by('-joined_at')
    serializer_class = MemberSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['member_id', 'name', 'phone_number'] 
    ordering_fields = ['joined_at', 'last_visited_at', 'points'] 
    ordering = ['-joined_at']  

    @action(detail=False, methods=["get"], url_path="generate-id")
    def generate_id(self, request):
        prefix = request.query_params.get("prefix")
        if not prefix:
            return Response(
                {"prefix query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            member_id = generate_member_id(prefix)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"member_id": member_id})

    @action(detail=True, methods=["post"], url_path="add-points")
    def add_points(self, request, pk=None):

        member = self.get_object()

        try:
            points = int(request.data.get("points", 0))
        except (TypeError, ValueError):
            return Response(
                {"detail": "points must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if points <= 0:
            return Response(
                {"detail": "points must be a positive integer."},
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
        POST members/{id}/use-points/
        body: { "points": 1000 }
        """
        member = self.get_object()

        try:
            amount = int(request.data.get("points", 0))
        except (TypeError, ValueError):
            return Response(
                {"detail": "points must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount <= 0:
            return Response(
                {"detail": "points must be a positive integer."},
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
                    {"detail": "Not enough points."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        member.refresh_from_db()
        serializer = self.get_serializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)