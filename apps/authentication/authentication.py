import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ecommerce.settings import mongo_db

class CustomUser:
    """
    A custom user object to wrap the MongoDB user dictionary.
    """

    def __init__(self, user_data):
        self.user_data = user_data
        self._id = user_data.get("_id")
    @property
    def pk(self):
        """
        Map the pk attribute to MongoDB's _id field.
        """
        return str(self._id)  # Convert ObjectId to string
    @property
    def email(self):
        return self.user_data.get("email")

    @property
    def role(self):
        return self.user_data.get("role", "customer")  

    @property
    def is_authenticated(self):
        return True


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the user using the JWT token in the Authorization header.
        """
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Authentication credentials were not provided.")

        token = auth_header.split(' ')[1]

        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = payload.get('email')

            # Fetch the user from MongoDB
            user = mongo_db['users'].find_one({"email": email})
            if not user:
                raise AuthenticationFailed("User not found.")

            return (CustomUser(user), None)  # Return the custom user object
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")