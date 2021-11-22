class Kakao:
    def __init__(self, access_token):
        self.access_token         = access_token
        self.user_information_url = "https://kapi.kakao.com/v2/user/me"
        self.map_url              = "https://kapi.kakao.com/v2/kakao-map/"

    @property
    def user_profile_information(self):
        response = requests.get(
            self.user_information_url
            headers = {'Authorization' : f'Bearer {self.access_token}'},
            timeout = 1
        )

        if not response.status_code == 200:
            raise Exception(..)

        return response.json()

    def get_current_address(self, lat, long):
        response = requests.get(self.map_url + f'?lattitude={self.lat}&logitutde={self.log}')

        return response


class KakaotalkSignInView(View):
    def get(self, request):
        try : 
            kakao      = Kokao(access_token = request.headers['Authorization'])
            kakao_user = kakao.user_profile_information

            user, created     = User.objects.get_or_create(
                social_id     = kakao_user["id"],
                defaults = {
                    "nickname" : kakao_user["properties"]["nickname"],
                    "email"    : kakao_user["kakao_account"]["email"]
                }
            )

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

            return JsonResponse({"access_token" : access_token}, status = 200)                
        
        except KeyError:
            return JsonResponse({"message" : "Key_Error"}, status = 401)
