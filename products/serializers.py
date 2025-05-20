from rest_framework import serializers

from products.models import Buy, Categories, Products


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', )


class BuySerializer(serializers.ModelSerializer):

    class Meta:
        model = Buy
        fields = ('product', 'quantity', 'total_buy')
        read_only_fields = ('total_buy',)

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity >= product.stock:
            raise serializers.ValidationError(
                {'product': f'{product.name}',
                 'stock': f'{product.stock}',
                 'erro': f'Não há estoque para o valor informado: {quantity}'}
            )
        return super().validate(data)

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                {'erro': 'O valor deve ser maior que ZERO.'}
            )
        return value

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']

        product.stock -= quantity
        product.save()
        return super().create(validated_data)
