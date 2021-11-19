from django.urls import path
from reviews.views import ReviewView

urlpatterns=[
    path('/review' , ReviewView.as_view()),
]