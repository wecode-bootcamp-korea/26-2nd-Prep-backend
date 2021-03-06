from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, F, Count, Q

from products.models import Category, Product, MainImage
from .models import Category, Product
from reviews.models import Review

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()

        result = [
            {
                'id'    : category.id,
                'name'  : category.name,
                'image' : category.image_url
            } for category in categories
        ]

        return JsonResponse({'result' : result}, status=200)

class ProductListView(View):
    def get(self, request):
        category          = request.GET.get("category_id")
        ordering          = request.GET.get("ordering")
        sub_category      = request.GET.get('sub_category_id')
        searching         = request.GET.get('searching')
        address           = request.GET.get('address')
        price_upper_range = request.GET.get('price_upper', 300000)
        price_lower_range = request.GET.get('price_lower', 0)
        OFFSET            = int(request.GET.get("offset", 0))
        LIMIT             = int(request.GET.get("limit", 12))

        q=Q()

        if category:
            q &= Q(sub_category__category_id = category)

        if sub_category:
            q &= Q(sub_category_id = sub_category)

        if address:
            q &= Q(address_id=address)

        if searching:
            q &= Q(sub_category__category__name__icontains = searching)|\
                 Q(sub_category__name__icontains = searching)|\
                 Q(name__icontains = searching)|\
                 Q(tags__name__icontains = searching)|\
                 Q(address__name__icontains = searching)

        q &= Q(discounted_price__range = (price_lower_range,price_upper_range))

        products = Product.objects.select_related('address')\
            .annotate(
                best_ranking     = Avg('option__review__star_rate'),
                review_count     = Count('option__review'),
                star_rate        = Avg('option__review__star_rate'),
                latest_update    = F('created_at'),
                discounted_price = F('option__price') - F('option__price') * (F('option__discount_rate')/100),
            )\
            .filter(q)\
            .order_by(ordering)[OFFSET:OFFSET+LIMIT]\
            .prefetch_related('option_set', 'option_set__review_set')\

        total_count = Product.objects.annotate(
                discounted_price = F('option__price') - F('option__price') * (F('option__discount_rate')/100)
        ).filter(q).values("id").distinct().count()

        results = [
            {
                'id'               : product.id,
                'product_name'     : product.name,
                'price'            : float(product.option_set.first().price),
                'discounted_price' : float(round(product.discounted_price,0)),
                'image_url'        : product.productimage_set.first().image_url,
                'star_point'       : float(round(product.star_rate,1)),
                'address'          : product.address.name,
                'tag'              : [tag.name for tag in product.tags.all()]
            }for product in products]

        return JsonResponse({'results':results, 'total_count' : total_count}, status = 200)

class MainImageView(View):
    def get(self, request):
        mainimages = MainImage.objects.all()

        results=[
            {
                'id' : mainimage.id,
                'image_url' : mainimage.image_url
            }for mainimage in mainimages
        ]

        return JsonResponse({'results' : results}, status = 200)

class ProductView(View) : 
    def get(self, request, product_id):
        try : 
            product       = Product.objects.annotate(star_rate = Avg('option__review__star_rate')).get(id=product_id)
            product_image = product.productimage_set.filter(product_id=product_id)
            

            result = {
                "product_info" :{
                    "name"              : product.name,
                    "product_image_url" : [productimage.image_url for productimage in product_image],
                    "expiration_date"   : product.expiration_date.name,
                    "address"           : product.address.name,
                    "tag"               : [tag.name for tag in product.tags.all()],
                    "average_rating"    : float(round(product.star_rate,2)),
                    "description"       : product.description
                },
                "option_list" :[{
                    "review_count"     : option.review_set.all().count(),
                    "stars_percent"    : option.review_set.filter(star_rate = 5).count()/option.review_set.all().count()*100 if option.review_set.all().count() != 0 else 0,
                    "name"             : option.name,
                    "price"            : float(option.price),
                    "discounted_price" : float(round((100-option.discount_rate)* option.price/100,2)),
                    "date"             : option.date,
                    "discount_rate"    : float(option.discount_rate),
                    "limited_quantity" : option.limited_quantity,
                    "reviews_list"     : [{
                        "star_rate"    : float(review.star_rate),
                        "comment"      : review.comment,
                    } for review in option.review_set.all()]
                } for option in product.option_set.all()]
            }
            return JsonResponse({"message" : result}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({"message" : "This device is does not exist"}, status=401)