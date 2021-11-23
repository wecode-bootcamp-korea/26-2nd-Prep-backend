from django.urls import path
from users.views import KakaotalkSignInView

urlpatterns = [
	path('/kakao', KakaotalkSignInView.as_view())
]