from django.urls import path

from . import views

urlpatterns = [
    path('products/', view=views.ProductCreateListView.as_view(),
         name='product-create-list'),

    path('products/<int:pk>/',
         view=views.ProductRetriverUpdateDestroyView.as_view(),
         name='product-detail-delete'),

    path('categories/', view=views.CategoriesCreateListView.as_view(),
         name='category-create-list'),

    path('categories/<int:pk>/',
         view=views.CategoryRetriverUpdateView.as_view(),
         name='category-detail-delete'),

    path('buy/', view=views.BuyCreateView.as_view(), name='buy-create'),


    path('cart/', view=views.CartListCreateView.as_view(), name='cart-create-list'),
    path("cart/<int:pk>/", view=views.CartRetrieveDestroyView.as_view(),
         name='cart-detail-destroy'),

    path('cart/items/', view=views.CartItemsListCreateView.as_view(),
         name='cart-item-create-list'),
    path('cart/items/<int:pk>/', view=views.CartItemsRetrieveDestroyView.as_view(),
         name='cart-item-create-list'),
]
