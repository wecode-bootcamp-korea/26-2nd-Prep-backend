import json, jwt, requests

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .models import User

class Kakao:
    def __init__(self,access_token) : 
        self.access_token = access_token
        self.user_information_api = "https://kapi.kakao.com/v2/user/me"

    # @property
    def get_user_profile_information(self):
        response = requests.get(self.user_information_api,
            headers = {'Authorization' : f'Bearer {self.access_token}'},
            timeout=5
        )

        if not response.status_code == 200:
            raise Exception('This access_token is not authorized!!')

        return response.json()