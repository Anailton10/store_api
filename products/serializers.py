from rest_framework import serializers

from products.models import Buy, Cart, CartItem, Categories, Products


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


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('product', 'cart', 'quantity',)
        read_only_fields = ('cart',)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                {'erro': 'Valor informado menor que zero'}
            )
        return value

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity > product.stock:
            raise serializers.ValidationError(
                {'quantity': 'Estoque insuficiente para quantidade informada',
                 'product': f'{product.name}'}
            )
        return data

    def create(self, validated_data):
        try:
            # Instanciando as fields validadas
            product = validated_data['product']
            cart = validated_data['cart']
            quantity = validated_data['quantity']

            # Buscando o item pelo id do carinho e do produto para ver se já tem registro
            item = CartItem.objects.filter(cart=cart, product=product).first()

            # Se item retornar none irá ter um 'novo registro'
            if item is None:
                return super().create(validated_data)

            # Se retorna algum item a quantidade do item irá ser somado ao item do carrinho
            else:
                item.quantity += quantity
                # Salvando o item
                item.save()
                return item
        except Exception as e:
            raise serializers.ValidationError(
                f'Occorreu um erro ao criar o item: {str(e)}')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'session_id', 'is_activate', 'product',)
        read_only_fields = ('user', 'session_id', 'is_activate',)
        items = CartItemSerializer(many=True, read_only=True)

    def create(self, validated_data):

        user = self.context['request'].user
        session = self.context['request'].session

        if user.is_authenticated:
            cart = Cart.objects.create(user=user)
        else:
            cart_id = session.get('cart_id')
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
            else:
                cart = Cart.objects.create()
                session['cart_id'] = cart_id
                return cart
