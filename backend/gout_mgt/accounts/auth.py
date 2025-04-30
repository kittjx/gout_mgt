
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from .tokens import Token

class TokenAuthentication(BaseTokenAuthentication):
    keyword = 'Bearer'
    model = Token
    
    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')

        if not header:
            print("No Authorization header found")
            return None

        try:
            auth = header.split()

            if len(auth) != 2 or auth[0].lower() != self.keyword.lower():
                print(f"Invalid auth format. Expected: {self.keyword} <token>")
                return None

            token_key = auth[1]
            
            token = self.model.objects.get(key=token_key)
            
            return (token.user, token)
        except (self.model.DoesNotExist, IndexError) as e:
            print("Authentication error:", str(e))
            return None
