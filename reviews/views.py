import json, boto3

from django.http import JsonResponse
from django.views import View

from .models import Review, ReviewImage, Like
from users.models import User
from products.models import  Option
from core.utils import signin_decorator
from django.conf  import settings

class LikeView(View):
    @signin_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            review_id = data['review_id']
        
            like, created = Like.objects.get_or_create(
                user_id = user_id,
                review_id = review_id
            )

            if not created:
                like.delete()

            review = Review.objects.get(id=review_id)
            results={
                    'likes' : len(review.like_set.all()),
                    'review_id' : review_id
            }

            return JsonResponse({'results' : results}, status=201)

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)