from django.urls import path
from reviews.views import ReviewView, LikeView

urlpatterns=[
    path('products/<int:id>/reviews/likes', LikeView.as_view())
]