from rest_framework import generics

from .models import Categories, Products
from .serializers import CategoriesSerializer, ProductsSerializer


class ProductCreateListView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class ProductRetriverUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class CategoriesCreateListView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class CategoryRetriverUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


# class BuyCreateView(generics.CreateAPIView):
#     queryset = Buy.objects.all()
#     serializer_class = BuySerializer
