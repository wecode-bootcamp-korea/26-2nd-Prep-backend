import jwt

from django.test import Client, TestCase
from django.conf import settings
from unittest.mock import MagicMock, patch

from .models import User

class KakaoLogIntest(TestCase):
    def setUp(self):
        User.objects.create(
            id            = 1, 
            social_id     = 1234567, 
            nickname      ='hi', 
            profile_image = "http://yyy.kakao.com/dn/.../img_640x640.jpg", 
            email         = "drageon@gmail.com")
    
    def tearDown(self):
        User.objects.all().delete()
    
    @patch('users.utils.Kakao.get_user_profile_information')
    def test_kakao_lonin_existing_view_success(self,mocked_requests):
        client = Client()

        mocked_response = {
            "id"            : 1234567,
            "properties"    : {
                "nickname"  : 'hi'
                },
            "kakao_account" : {
                "profile"   : {
                    "profile_image_url" : "http://yyy.kakao.com/dn/.../img_640x640.jpg"
                    },
                "email" : "drageon@gmail.com",
            }
        }

                
        mocked_requests.return_value = mocked_response
        headers             = {"HTTP_Authorization" : "fake_siteToken"}
        response            = client.get("/users/kakao", **headers)
        jwt_token           = jwt.encode({"id" : 1}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Token" : jwt_token})

    @patch('users.utils.Kakao.get_user_profile_information')
    def test_kakao_lonin_creating_view_success(self,mocked_requests):
        client = Client()

        mocked_response = {
            "id" : 12345678,
            "properties" : {
                "nickname" : 'bye'
                },
            "kakao_account" : {
                "profile"   : {
                    "profile_image_url" : "http://yyy.kakao.com/dn/.../img_640x640.jpg"
                },
                "email" : "drageonlee@gmail.com",
            }
        }   
                
        mocked_requests.return_value = mocked_response
        headers             = {"HTTP_Authorization" : "fake_siteToken"}
        response            = client.get("/users/kakao", **headers)
        jwt_token           = jwt.encode({"id" : 2}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Token" : jwt_token})

    def test_kakao_lonin_creating_view_no_access_token_fail(self):
        client = Client()

        headers             = {}
        response            = client.get("/users/kakao", **headers)
        jwt_token           = jwt.encode({"id" : 1}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{"message" : "Key_Error"})