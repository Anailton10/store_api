from rest_framework import serializers

from products.models import Categories, Products


class ProductsSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Products
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = (
            'id',
            'name',
        )
