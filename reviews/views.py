import json, boto3, uuid

from django.http            import JsonResponse
from django.views           import View
from django.db              import transaction
from django.conf            import settings
from django.db.models       import Count
from django.core.exceptions import ValidationError

from .models         import Review, ReviewImage, Like
from users.models    import User
from products.models import Option
from core.utils      import signin_decorator
from utils           import FileUpload

class ReviewView(View):
    @signin_decorator
    def post(self, request):
        try:
            comment    = request.POST['comment']
            user_id    = request.user.id
            star_rate  = request.POST['star_rate']
            option_id  = request.POST['option_id']

            file = FileUpload(file=request.FILES['filename'])
            file_url = file.upload_file()            

            with transaction.atomic():
                review=Review.objects.create(
                    option_id = option_id,
                    star_rate = star_rate,
                    user_id   = user_id,
                    comment   = comment
                )

                if file_url:
                    ReviewImage.objects.create(
                        review_id = review.id,
                        image_url = file_url
                    )

                return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except ValidationError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    def get(self, request):
        try:
            product_id = request.GET.get('product_id')
            
            reviews = Review.objects.annotate(likes = Count('like')).filter(option_id__product__id = product_id).prefetch_related('reviewimage_set')

            results=[
                {
                    'id'                 : review.id,
                    'user_nickname'      : review.user.nickname,
                    'user_profile_image' : review.user.profile_image,
                    'option_name'        : review.option.name,
                    'comment'            : review.comment,
                    'likes'              : review.likes,
                    'option_date'        : review.option.date,
                    'review_image'       : [reviewimage.image_url for reviewimage in review.reviewimage_set.all()],
                    'star_rate'          : float(review.star_rate)
                } for review in reviews
            ]

            return JsonResponse({'results' : results}, status=200)

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

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