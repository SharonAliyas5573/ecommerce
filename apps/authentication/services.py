from django.conf import settings
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from ecommerce.settings import mongo_db
# MongoDB collection for users
users_collection = mongo_db['users']

SECRET_KEY = settings.SECRET_KEY

def register_user(email, password, role="customer"):
    """
    Registers a new user in the MongoDB database.
    """
    if role not in ["admin", "customer"]:
        raise ValidationError("Invalid role. Role must be 'admin' or 'customer'.")

    hashed_password = generate_password_hash(password)
    user_data = {
        "email": email,
        "password": hashed_password,
        "role": role,  # Add role field
    }

    try:
        settings.mongo_db['users'].insert_one(user_data)
        return {"success": True, "message": "User registered successfully."}
    except DuplicateKeyError:
        return {"success": False, "message": "Email already exists."}
        
def generate_jwt_token(email):
    """
    Generates an access and refresh token for the user.
    """
    access_token_payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),  # Access token expires in 15 minutes
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token_payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),  # Refresh token expires in 7 days
        "iat": datetime.datetime.utcnow(),
    }

    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm="HS256")

    return access_token, refresh_token

def authenticate_user(email, password):
    """
    Authenticates a user by checking their email and password.
    Returns JWT tokens if authentication is successful.
    """
    user = users_collection.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        # Generate JWT tokens
        access_token, refresh_token = generate_jwt_token(email)
        return {
            "success": True,
            "message": "Authentication successful.",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    return {"success": False, "message": "Invalid email or password."}