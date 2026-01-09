from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MemberViewSet

# DRF의 Router를 사용하면 CRUD용 URL을 자동으로 만들어줌
router = DefaultRouter()
router.register(r'', MemberViewSet, basename='member')
# 여기서 r'' 로 등록하고, config에서 "/members/"로 include 할 거라서
# 최종 URL은 /api/members/ , /api/members/{id}/ 이런 식이 됨

urlpatterns = []
urlpatterns += router.urls