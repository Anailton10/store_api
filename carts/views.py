from django.core import exceptions
from rest_framework import generics

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


class CartListView(generics.ListAPIView):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartDestroyView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemsListCreateView(generics.ListCreateAPIView):

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
                    user=user, is_activate=True)
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
            raise exceptions.ValidationError(f"Ocorreu um erro: {str(e)}")


class CartItemsRetrieveDestroyView(generics.RetrieveDestroyAPIView):

    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
