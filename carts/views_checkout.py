# from django.db import transaction
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from products.serializers import BuySerializer

# from .models import Cart, CartItem


# class CheckoutView(APIView):
#     def post(self, request):
#         user = request.user
#         session = request.session

#         try:
#             if not user.is_authenticated:
#                 return Response({'erro': 'Usuário precisa estar logado para finalizar a compra'}, status=status.HTTP_401_UNAUTHORIZED)

#             cart = Cart.objects.filter(user=user, is_activate=True).first()

#             cart_items = CartItem.objects.filter(cart=cart)

#             if not cart:
#                 return Response({'erro': "Carrinho não encontrado"}, status=status.HTTP_404_NOT_FOUND)

#             if not cart_items.exists():
#                 return Response({'erro': 'Carrinho está vazio.'}, status=status.HTTP_400_BAD_REQUEST)

#             # transaction.atomic garante que todas as movimentações sejam feitas, caso contrário não acontece nenhuma transação
#             with transaction.atomic():
#                 for item in cart_items:
#                     # Prepara os dados da compra com ID do produto e quantidade
#                     buy_data = {
#                         'product': item.product.id,
#                         'quantity': item.quantity,
#                     }

#                     # Instancia o serializer da compra para validar os dados e salvar
#                     serializer = BuySerializer(data=buy_data)
#                     if serializer.is_valid():
#                         serializer.save()
#                     else:
#                         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#                     # Marca o carrinho como finalizado para evitar reutilização futura
#                     cart.is_activate = False
#                     cart.save()

#                 if not user.is_authenticated:
#                     session.pop('cart_id', None)
#                     session.save()

#             return Response({'mensagem': 'Compra realizado com sucesso.'}, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"Erro": f"Ocorreu um erro {str(e)}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
