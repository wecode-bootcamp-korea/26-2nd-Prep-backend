from django.urls import path
from products.views import CategoryListView, ProductListView, ProductView,  MainImageView

urlpatterns=[
    path('categories', CategoryListView.as_view()),
    path('products', ProductListView.as_view()),
    path('mainimages', MainImageView.as_view()),
    path('products/<int:product_id>', ProductView.as_view())
]