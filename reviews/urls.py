from django.urls import path
from reviews.views import ReviewView, LikeView

urlpatterns=[
    path('/review' , ReviewView.as_view()),
    path('/review/like', LikeView.as_view())
]