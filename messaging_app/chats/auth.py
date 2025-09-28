# Minimal auth helpers (required filename present). No extra logic beyond simple helper.
from rest_framework_simplejwt.authentication import JWTAuthentication

def get_jwt_authenticator():
    """
    Return a JWTAuthentication instance (helper function).
    Kept minimal and explicit as per objective.
    """
    return JWTAuthentication()
