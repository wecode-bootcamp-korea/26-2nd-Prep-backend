import unittest, json, jwt

from django.test import Client, TestCase
from unittest.mock import MagicMock, Mock, patch
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import User

class KakaoLogIntest(TestCase):
    def setUp(self):
        User.objects.create(id=1, social_id = 1234567, nickname='hi', profile_image = "http://yyy.kakao.com/dn/.../img_640x640.jpg", email="drageon@gmail.com")
    
    def tearDown(self):
        User.objects.all().delete()
    
    @patch("users.views.requests")
    def test_kakao_lonin_existing_view_success(self,mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self) : 
                return {
                    "id" : 1234567,
                    "properties" : {
                        "nickname" : "hi"
                        },
                    "kakao_account" : {
                        "profile" : {
                            "profile_image_url" : "http://yyy.kakao.com/dn/.../img_640x640.jpg"
                        },
                        "email" : "drageon@gmail.com",
                    }
                }   
                
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"Authorization" : "fake_siteToken"}
        response            = client.get("/users/kakao", **headers)
        siteToken           = jwt.encode({"id" : 1}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Token" : siteToken})

    @patch("users.views.requests")
    def test_kakao_lonin_creating_view_success(self,mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self) : 
                return {
                    "id" : 12345678,
                    "properties" : {
                        "nickname" : "hi"
                        },
                    "kakao_account" : {
                        "profile" : {
                            "profile_image_url" : "http://yyy.kakao.com/dn/.../img_640x640.jpg"
                        },
                        "email" : "drageon@gmail.com",
                    }
                }   
                
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"Authorization" : "fake_siteToken"}
        response            = client.get("/users/kakao", **headers)
        siteToken           = jwt.encode({"id" : 2}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"Token" : siteToken})

    def test_kakao_lonin_creating_view_no_access_token_fail(self):
        client = Client()

        headers             = {}
        response            = client.get("/users/kakao", **headers)
        siteToken           = jwt.encode({"id" : '1'}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        self.assertEqual(response.status_code, 401)