from django.urls import path

from . import views

urlpatterns = [
    path('cart/', view=views.CartListView.as_view(), name='cart-create-list'),
    path("cart/<int:pk>/", view=views.CartDestroyView.as_view(),
         name='cart-detail-destroy'),

    path('cart/items/', view=views.CartItemsListCreateView.as_view(),
         name='cart-item-create-list'),
    path('cart/items/<int:pk>/', view=views.CartItemsRetrieveDestroyView.as_view(),
         name='cart-item-create-list'),
]
