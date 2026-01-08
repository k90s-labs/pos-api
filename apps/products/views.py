from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductDetailSerializer


@api_view(["GET"])
def product_detail(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)
