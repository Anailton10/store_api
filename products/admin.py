from django.contrib import admin

from .models import Categories, Products


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'cart', 'product', 'quantity')
#     list_filter = ('cart', 'product')
#     search_fields = ('cart__id', 'product__name')
