from django.urls import path

from . import views

urlpatterns = [
    path('cart/', view=views.CartListCreateView.as_view(), name='cart-create-list'),
    path("cart/<int:pk>/", view=views.CartRetrieveDestroyView.as_view(),
         name='cart-detail-destroy'),

    path('cart/items/', view=views.CartItemsListCreateView.as_view(),
         name='cart-item-create-list'),
    path('cart/items/<int:pk>/', view=views.CartItemsRetrieveDestroyView.as_view(),
         name='cart-item-create-list'),
]
