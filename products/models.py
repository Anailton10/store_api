from django.contrib.auth.models import User
from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Products(models.Model):

    name = models.CharField(max_length=30)
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, default='')
    price = models.DecimalField(decimal_places=2, max_digits=8)
    stock = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Buy(models.Model):

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_buy = models.DecimalField(
        decimal_places=2, max_digits=10, blank=True)

    def save(self, *args, **kwargs):  # O save é usando quando o objeto vai ser salvo no Banco de Dados
        self.total_buy = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity} unidades"


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
