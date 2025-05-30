from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Categories, Products
from .serializers import CategoriesSerializer, ProductsSerializer


class ProductCreateListView(generics.ListCreateAPIView):

    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    # Dar permissão para qualquer usuário com SAFE METHOD
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class ProductRetriverUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class CategoriesCreateListView(generics.ListCreateAPIView):

    permission_classes = (IsAdminUser,)
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class CategoryRetriverUpdateView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAdminUser,)
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


# class BuyCreateView(generics.CreateAPIView):
#     queryset = Buy.objects.all()
#     serializer_class = BuySerializer
