from django.urls import path
from .views import product_detail

# Django의 urls.py는 “이 URL이 오면 → 이 함수로 보내라” 라는 순수 매핑 테이블.
# 브라우저 / 클라이언트
#    ↓
# config/urls.py   ← (프로젝트 진입점)
#    ↓ include()
# products/urls.py ← (도메인별 분기)
#    ↓
# views.py         ← (실제 로직)


urlpatterns = [
    path("<int:product_id>/", product_detail, name="product-detail"),
]
