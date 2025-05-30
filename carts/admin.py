from django.contrib import admin

from .models import Buy, Cart, CartItem


# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'is_activate', 'created_at')
    list_filter = ('is_activate', 'created_at')
    search_fields = ('user__username', 'session_id')
    inlines = [CartItemInline]


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'total_buy')
    list_filter = ('product',)
    search_fields = ('product__name',)
