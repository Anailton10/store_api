from django.core import exceptions
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import (
    BuySerializer,
    CartHistorySerializer,
    CartItemSerializer,
    CartSerializer,
)


class CartListView(generics.ListAPIView):

    permission_classes = (AllowAny,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    # Apenas o propio usuario pode acessar seu carrinho
    def get_queryset(self):
        user = self.request.user
        session = self.request.session
        if user.is_authenticated:
            return Cart.objects.filter(user=user, is_activate=True)
        else:
            cart_id = session.get('cart_id')
            return Cart.objects.filter(session_id=cart_id, is_activate=True)


class CartHistoryView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartHistorySerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user, is_activate=False).order_by(
            '-created_at'
        )


class CartDestroyView(generics.DestroyAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemsListCreateView(generics.ListCreateAPIView):

    permission_classes = (AllowAny,)
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    # função para customizar o que acontece após a validação do serializer
    def perform_create(self, serializer):
        request = self.request
        user = request.user
        session = request.session

        if not session.session_key:
            session.save()  # força a criação da sessão se necessário

        try:
            if user.is_authenticated:
                cart, _ = Cart.objects.get_or_create(
                    user=user, is_activate=True
                )
            else:
                cart_id = session.get('cart_id')
                if cart_id:
                    try:
                        cart = Cart.objects.get(id=cart_id, user__isnull=True)
                    except Cart.DoesNotExist:
                        pass
                else:
                    cart = Cart.objects.create(session_id=session.session_key)
                    session['cart_id'] = cart.id
                    session.save()  # salva para garantir persistência
            serializer.save(cart=cart)

        except Exception as e:
            raise exceptions.ValidationError(f'Ocorreu um erro: {str(e)}')


class CartItemsRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartCheckoutView(APIView):

    permission_classes = (IsAuthenticated,)

    # Apenas o propio usuario pode fazer seu checkout
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user, is_activate=True)

    def post(self, request):
        user = request.user

        try:
            if not user.is_authenticated:
                return Response(
                    {
                        'erro': 'Usuário precisa estar logado para finalizar a compra'
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            cart = Cart.objects.filter(user=user, is_activate=True).first()

            cart_items = CartItem.objects.filter(cart=cart)

            if not cart:
                return Response(
                    {'erro': 'Carrinho não encontrado'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not cart_items.exists():
                return Response(
                    {'erro': 'Carrinho está vazio.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # transaction.atomic garante que todas as movimentações sejam feitas, caso contrário não acontece nenhuma transação
            with transaction.atomic():
                for item in cart_items:
                    # Prepara os dados da compra com ID do produto e quantidade
                    buy_data = {
                        'product': item.product.id,
                        'cart': item.cart,
                        'quantity': item.quantity,
                        'total_buy': item.product.price * item.quantity,
                    }

                    # Instancia o serializer da compra para validar os dados e salvar
                    serializer = BuySerializer(data=buy_data)
                    if serializer.is_valid():
                        serializer.save(cart=cart)
                    else:
                        return Response(
                            serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # Marca o carrinho como finalizado para evitar reutilização futura
                    cart.is_activate = False
                    cart.save()

            return Response(
                {'mensagem': 'Compra realizado com sucesso.'},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {'Erro': f'Ocorreu um erro {str(e)}.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
