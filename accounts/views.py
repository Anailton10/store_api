from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import UserRegisterSeriliazer


class UserRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSeriliazer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                "message": "Usuário cadastrado com sucesso!",
                "user": response.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "message": "Usuário não cadastrado!",
                'erro': f'Ocorreu um erro: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
