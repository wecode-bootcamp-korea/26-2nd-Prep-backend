import json, jwt, requests

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .models import User

class KakaotalkSignInView(View):
    def get(self, request):
        try : 
            ACCESS_TOKEN        = request.headers.get('Authorization')
            profile_information = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers = {'Authorization' : f'Bearer {ACCESS_TOKEN}'}
            )

            profile_information_json = profile_information.json()
            print(profile_information_json)
            profile_id               = profile_information_json["id"]
            email                    = profile_information_json["kakao_account"]["email"] 
            nickname                 = profile_information_json["properties"]["nickname"]
            profile_image            = profile_information_json["kakao_account"]["profile"]["profile_image_url"]

            user, created     = User.objects.get_or_create(
                social_id     = profile_id,
                nickname      = nickname,
                email         = email,
                profile_image = profile_image)
            siteToken         = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            
            if created: 
                return JsonResponse({"Token" : siteToken}, status = 201)
            else: 
                return JsonResponse({"Token" : siteToken}, status = 200)
                    
        except KeyError:
            return JsonResponse({"message" : "This access token does not exist"}, status = 401)

        except User.DoesNotExist:
            return JsonResponse({"message" : "Does_Not_Exist"}, status=404)