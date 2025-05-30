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
]
