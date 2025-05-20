from django.core import exceptions
from rest_framework import generics

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


class CartListCreateView(generics.ListCreateAPIView):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemsListCreateView(generics.ListCreateAPIView):

    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    # função ideal para customizar o que acontece após a validação do serializer
    def perform_create(self, serializer):
        try:
            request = self.request
            user = request.user
            session = request.session

            if user.is_authenticated:
                try:
                    cart = Cart.objects.get(user=user)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(user=user)
            else:
                cart_id = session.get('cart_id')
                if cart_id:
                    cart = Cart.objects.get(id=cart_id)
                else:
                    cart = Cart.objects.create()
                    session['cart_id'] = cart.id
            serializer.save(cart=cart)
        except Cart.DoesNotExist:
            raise exceptions.ValidationError('Carrinho não encontrado')
        except Exception as e:
            raise exceptions.ValidationError(
                f"Ocorreu um erro ao adicionar o item: {str(e)}")


class CartItemsRetrieveDestroyView(generics.RetrieveDestroyAPIView):

    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
