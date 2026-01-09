from rest_framework import viewsets, filters

from .models import Member
from .serializers import MemberSerializer


class MemberViewSet(viewsets.ModelViewSet):
    """
    Member CRUD를 담당하는 ViewSet

    자동으로 지원되는 것:
    - GET /members/        → 리스트 조회
    - GET /members/{id}/   → 상세 조회
    - POST /members/       → 생성
    - PUT /members/{id}/   → 전체 수정
    - PATCH /members/{id}/ → 부분 수정
    - DELETE /members/{id}/ → 삭제
    """
    queryset = Member.objects.all().order_by('-joined_at')
    serializer_class = MemberSerializer

    # 🔍 검색 & 정렬 설정
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['member_id', 'name', 'phone_number']  # 여기 포함된 필드들 대상으로 검색
    ordering_fields = ['joined_at', 'last_visited_at', 'points']  # 정렬 허용 필드
    ordering = ['-joined_at']  # 기본 정렬 기준