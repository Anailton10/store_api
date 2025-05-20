from django.contrib import admin

from .models import Cart, CartItem


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
