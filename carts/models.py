from django.contrib.auth.models import User
from django.db import models

from products.models import Products


class Cart(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True,)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    # True - carrinho novo / False - carrinho encerrado
    is_activate = models.BooleanField(default=True)
    product = models.ManyToManyField(Products, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()

    class Meta:

        unique_together = ('product', 'cart',)


class Buy(models.Model):

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart')
    quantity = models.PositiveIntegerField()
    total_buy = models.DecimalField(
        decimal_places=2, max_digits=10, blank=True)

    def save(self, *args, **kwargs):  # O save é usando quando o objeto vai ser salvo no Banco de Dados
        self.total_buy = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity} unidades"
