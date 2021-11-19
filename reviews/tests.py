import json, jwt

from django.test                    import TestCase, Client
from unittest.mock                  import MagicMock, patch
from django.conf                    import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from .models         import Review, ReviewImage, Like
from users.models    import User
from products.models import Product, Option, Category, SubCategory, ExpirationDate, ProductAddress
from utils           import FileUpload

class ReviewTest(TestCase):
    def setUp(self):
        User.objects.create(id=1, social_id=11, nickname='짱민석', profile_image='aa', email='ipod1011@naver.com', phone_number='01032678777')

        self.token = jwt.encode({'id' : User.objects.get(id=1).id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

        Category.objects.create(id=1, name='아웃도어')

        SubCategory.objects.create(id=1, name='등산', category_id=1)

        ExpirationDate.objects.create(id=1, name='구매일로부터 30일까지')

        ProductAddress.objects.create(id=1, name='서울')

        Product.objects.create(id=1, name='야외 바베큐', address_id=1, expiration_date_id=1, sub_category_id=1)

        Option.objects.create(id=1, name='참가비(1인)', date='2021-11-30', price=10000, discount_rate=0, limited_quantity=24, product_id=1)

        review_list=[
            Review(
                id        =1,
                option_id =1,
                user_id   =1,
                star_rate =1,
                comment   ='aa'
            ),
            Review(
                id        =2,
                option_id =1,
                user_id   =1,
                star_rate =2,
                comment   ='bb'
            ),
            Review(
                id        =3,
                option_id =1,
                user_id   =1,
                star_rate =3,
                comment   ='cc'
            )
        ]

        Review.objects.bulk_create(review_list)

        review_image_list=[
            ReviewImage(
                id        =1,
                review_id =1,
                image_url ='aa'
            ),
            ReviewImage(
                id        =2,
                review_id =2,
                image_url ='bb'
            ),
            ReviewImage(
                id        =3,
                review_id =3,
                image_url ='cc'
            ) 
        ]

        ReviewImage.objects.bulk_create(review_image_list)

        like_list =[
            Like(
                id        =1,
                review_id =1,
                user_id   =1
            ),
            Like(
                id        =2,
                review_id =2,
                user_id   =1
            )
        ]

        Like.objects.bulk_create(like_list)

    def tearDown(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        Option.objects.all().delete()
        Review.objects.all().delete()
        ReviewImage.objects.all().delete()
        Like.objects.all().delete()
        ProductAddress.objects.all().delete()
        ExpirationDate.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()

    @patch('utils.FileUpload')
    def test_Review_post_success(self, mocked_requests):
        client = Client()
       
        review = {
            'comment'   : 'bb',
            'star_rate' : 2,
            'option_id' : 1,
            'user_id'   : 1,
            'filename'  : SimpleUploadedFile(
                name = 'test.png',
                content = b'file_content',
                content_type = 'image/jpeg'
            )
        }

        class MockedResponse:
            def upload_fileobj(self):
                return 'aa'

        mocked_requests.upload_fileobj = MagicMock(return_value = MockedResponse())
        print(mocked_requests)
        headers  = {'HTTP_Authorization' : self.token}
        response = client.post('/reviews/review', review, ContentType='mulitpart/form-data', **headers)
        self.assertEqual(response.json(),{'message' : 'SUCCESS'})
        self.assertEqual(response.status_code, 201)

    def test_Review_post_key_error(self):
        client = Client()
        body = {
            'filename'  : 'aa',
            'comment'   : 'bb',
            'star_rate' : 2,
            'option_id' : 1,
            'user_id'   : 1
        }
        headers  = {'HTTP_Authorization' : self.token}
        response = client.post('/reviews/review', body, **headers)
        self.assertEqual(response.json(),{'message' : 'KEY_ERROR'})
        self.assertEqual(response.status_code, 400)

    def test_Review_get_sucess(self):
        client = Client()
        response = client.get('/reviews/review?product_id=1')
        self.assertEqual(response.json(),
            {
                'results' : [
                    {
                        'id'                 : 1,
                        'user_nickname'      : '짱민석',
                        'user_profile_image' : 'aa',
                        'option_name'        : '참가비(1인)',
                        'comment'            : 'aa',
                        'likes'              : 1,
                        'option_date'        : '2021-11-30T00:00:00Z',
                        'review_image'       : ['aa'],
                        'star_rate'          : 1.0
                    },
                    {
                        'id'                 : 2,
                        'user_nickname'      : '짱민석',
                        'user_profile_image' : 'aa',
                        'option_name'        : '참가비(1인)',
                        'comment'            : 'bb',
                        'likes'              : 1,
                        'option_date'        : '2021-11-30T00:00:00Z',
                        'review_image'       : ['bb'],
                        'star_rate'          : 2.0
                    },
                    {
                        'id'                 : 3,
                        'user_nickname'      : '짱민석',
                        'user_profile_image' : 'aa',
                        'option_name'        : '참가비(1인)',
                        'comment'            : 'cc',
                        'likes'              : 0,
                        'option_date'        : '2021-11-30T00:00:00Z',
                        'review_image'       : ['cc'],
                        'star_rate'          : 3.0
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)