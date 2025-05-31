from rest_framework import serializers

from .models import Buy, Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.CharField(
        source='product.price', read_only=True)

    class Meta:
        model = CartItem
        fields = ('cart', 'product', 'product_name',
                  'product_price', 'quantity',)
        read_only_fields = ('cart',)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                {'erro': 'Valor informado menor que zero'}
            )
        return value

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']

        if quantity > product.stock:
            raise serializers.ValidationError(
                {'quantity': 'Estoque insuficiente para quantidade informada',
                 'product': f'{product.name}'}
            )
        return attrs

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

    total = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Cart
        fields = ('id', 'user', 'session_id',
                  'is_activate', 'items', 'total',)
        read_only_fields = ('user', 'session_id', 'is_activate',)
        cart_items = CartItemSerializer(many=True, read_only=True)

    def get_total(self, obj):
        items = CartItem.objects.filter(cart=obj)
        total_cart = sum(item.product.price *
                         item.quantity for item in items)
        return total_cart

    def get_items(self, obj):
        items = CartItem.objects.filter(cart=obj)
        return CartItemSerializer(items, many=True).data

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
                session['cart_id'] = cart.id
                session.save()
                return cart


class BuySerializer(serializers.ModelSerializer):

    class Meta:
        model = Buy
        fields = ('product', 'quantity', 'total_buy')
        read_only_fields = ('total_buy',)

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']

        if quantity >= product.stock:
            raise serializers.ValidationError(
                {'product': f'{product.name}',
                 'stock': f'{product.stock}',
                 'erro': f'Não há estoque para o valor informado: {quantity}'}
            )
        return super().validate(attrs)

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
