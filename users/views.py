import json, jwt, requests

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .models import User
from .utils import Kakao

class KakaotalkSignInView(View):
    def get(self, request):
        try :
            kakao      = Kakao(access_token = request.headers['Authorization'])
            kakao_user = kakao.get_user_profile_information

            user, created     = User.objects.get_or_create(
                nickname      = kakao_user['properties']['nickname'],
                email         = kakao_user['kakao_account']['email'],
                profile_image = kakao_user['kakao_account']['profile']['profile_image_url'],
                defaults = {"social_id" : kakao_user['id']})

            jwt_token         = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

            return JsonResponse({"Token" : jwt_token}, status = 200)
        
        except KeyError:
            return JsonResponse({"message" : "Key_Error"}, status = 401)