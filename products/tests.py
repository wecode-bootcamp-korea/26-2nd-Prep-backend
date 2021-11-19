import json

from django.test import TestCase
from django.test import Client

from .models     import Category, SubCategory, Product, ProductImage, Option, ProductAddress, ExpirationDate, Tag, ProductTag
from users.models import User
from reviews.models import Review

class CategoryTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id = 1,
            name = '아웃도어',
            image_url = 'https://images.unsplash.com/photo-1501555088652-021faa106b9b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1473&q=80'
        )

        Category.objects.create(
            id = 2,
            name = '피트니스',
            image_url = 'https://images.unsplash.com/photo-1579126038374-6064e9370f0f?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1431&q=80'
        )

        Category.objects.create(
            id=3,
            name = '공예DIY',
            image_url = 'https://images.unsplash.com/photo-1488806374796-a4071c52353b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1470&q=80'
        )

    def tearDown(self):
        Category.objects.all().delete()

    def test_Category_get_success(self):
        client = Client()
        response = client.get('/categories')
        self.assertEqual(response.json(),
            {
                'result' : [
                    {
                        'id': 1,
                        'image': 'https://images.unsplash.com/photo-1501555088652-021faa106b9b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1473&q=80',
                        'name': '아웃도어'
                    },
                    {
                        'id': 2,
                        'image': 'https://images.unsplash.com/photo-1579126038374-6064e9370f0f?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1431&q=80',
                        'name': '피트니스'
                    },
                    {
                        'id': 3,
                        'image': 'https://images.unsplash.com/photo-1488806374796-a4071c52353b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1470&q=80',
                        'name' : '공예DIY'
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_Category_get_url_error(self):
        client = Client()
        response = client.get('/asd')
        self.assertEqual(response.status_code, 404)

class ProductTest(TestCase):
    def setUp(self):
        User.objects.create(id=1,social_id=11, nickname='짱민석', profile_image='aa', email='ipod1011@naver.com', phone_number='01032678777')

        category_list=[
            Category(
                id = 1,
                name = '아웃도어',
                image_url = 'https://images.unsplash.com/photo-1501555088652-021faa106b9b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1473&q=80'
            ),
            Category(
                id = 2,
                name = '피트니스',
                image_url = 'https://images.unsplash.com/photo-1579126038374-6064e9370f0f?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1431&q=80'
            ),
            Category(
                id=3,
                name = '공예DIY',
                image_url = 'https://images.unsplash.com/photo-1488806374796-a4071c52353b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1470&q=80'
            )
        ]
        Category.objects.bulk_create(category_list)

        sub_category_list=[
            SubCategory(
                id=1,
                name = '캠핑',
                category_id = 1
            ),
            SubCategory(
                id=2,
                name= '등산',
                category_id = 1
            ),
            SubCategory(
                id=3,
                name= '도보여행',
                category_id=1
            )
        ]
        SubCategory.objects.bulk_create(sub_category_list)

        ExpirationDate.objects.create(id=1, name='구매일로부터 30일까지')

        address_list=[
            ProductAddress(
                id=1,
                name='서울'
            ),
            ProductAddress(
                id=2,
                name='인천'
            ),
            ProductAddress(
                id=3,
                name='대전'
            )
        ]

        ProductAddress.objects.bulk_create(address_list)

        product_list=[
            Product(
                id=1,
                name = '2030 국내최초 1박2일 불멍스키 혼펜_따로 또 같이',
                address_id = 1,
                expiration_date_id = 1,
                sub_category_id=1
            ),
            Product(
                id=2,
                name='싱싱캠핑 가을 감성 캠핑에 싱가포르 얹기:피노키오숲',
                address_id=2,
                expiration_date_id=1,
                sub_category_id=1
            ),
            Product(
                id=3,
                name='특별이벤트 피노키오숲, 마지막 야외 바베큐 그리고 표고버섯 키트까지',
                address_id=3,
                expiration_date_id=1,
                sub_category_id=1
            )
        ]
        
        Product.objects.bulk_create(product_list)

        option_list=[
            Option(
                id=1,
                name='참가비(1인)',
                date='2021-11-30',
                price= 159000,
                discount_rate=0,
                limited_quantity=24,
                product_id=1
            ),
            Option(
                id=2,
                name='참가비(1인)',
                date='2021-12-30',
                price= 170000,
                discount_rate=26,
                limited_quantity=17,
                product_id=2
            ),
            Option(
                id=3,
                name='[유스호스텔 숙박] 참가비(1인)',
                date='2021-12-30',
                price = 170000,
                discount_rate=18,
                limited_quantity=14,
                product_id=3
            )
        ]
        
        Option.objects.bulk_create(option_list)

        review_list=[
            Review(
                id=1,
                option_id=1,
                user_id=1,
                star_rate=1,
                comment='aa'
            ),
            Review(
                id=2,
                option_id=2,
                user_id=1,
                star_rate=2,
                comment='bb'
            ),
            Review(
                id=3,
                option_id=3,
                user_id=1,
                star_rate=3,
                comment='cc'
            )
        ]

        Review.objects.bulk_create(review_list)

        product_image_list=[
            ProductImage(
                id=1,
                image_url='aa',
                product_id=1
            ),
            ProductImage(
                id=2,
                image_url='bb',
                product_id=2
            ),
            ProductImage(
                id=3,
                image_url='cc',
                product_id=3
            )
        ]

        ProductImage.objects.bulk_create(product_image_list)

        Tag.objects.create(id=1, name='Only')

        ProductTag.objects.create(id=1, product_id=1, tag_id=1)
        ProductTag.objects.create(id=2, product_id=2, tag_id=1)

    def test_Product_get_searching_ordering_best_ranking_success(self):
        client = Client()
        response = client.get('/products?ordering=-best_ranking&searching=only')
        self.assertEqual(response.json(),
            {
                'results' :[
                    {
                        'id' : 2,
                        'product_name' : '싱싱캠핑 가을 감성 캠핑에 싱가포르 얹기:피노키오숲',
                        'price' : 170000.0,
                        'discounted_price' : 125800.0,
                        'image_url' : 'bb',
                        'star_point' : 2.0,
                        'address' : '인천',
                        'tag' : ['Only']
                    },
                    {
                        'id' : 1,
                        'product_name' : '2030 국내최초 1박2일 불멍스키 혼펜_따로 또 같이',
                        'price' : 159000.0,
                        'discounted_price' : 159000.0,
                        'image_url' : 'aa',
                        'star_point' : 1.0,
                        'address' : '서울',
                        'tag' : ['Only']
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_Product_get_address_ordering_review_count_success(self):
        client = Client()
        response = client.get('/products?ordering=-review_count&address=1')
        self.assertEqual(response.json(),
            {
                'results' :[
                    {
                        'id' : 1,
                        'product_name' : '2030 국내최초 1박2일 불멍스키 혼펜_따로 또 같이',
                        'price' : 159000.0,
                        'discounted_price' : 159000.0,
                        'image_url' : 'aa',
                        'star_point' : 1.0,
                        'address' : '서울',
                        'tag' : ['Only']
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_Product_get_url_error(self):
        client = Client()
        response = client.get('/asd')
        self.assertEqual(response.status_code, 404)