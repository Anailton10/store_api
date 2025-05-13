from django.contrib import admin
from .models import Categories, Products, Buy, Cart, CartItem


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'total_buy')
    list_filter = ('product',)
    search_fields = ('product__name',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'is_activate', 'created_at')
    list_filter = ('is_activate', 'created_at')
    search_fields = ('user__username', 'session_id')
    inlines = [CartItemInline]


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'cart', 'product', 'quantity')
#     list_filter = ('cart', 'product')
#     search_fields = ('cart__id', 'product__name')
