from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication

class CustomAuthentication(JWTAuthentication, SessionAuthentication):
    """
    Custom authentication class combining JWT and Session Authentication.
    DRF normally supports multiple authentication classes separately,
    but you can combine here if needed.
    """
    def authenticate(self, request):
        # Try JWT auth first
        jwt_auth = JWTAuthentication()
        user_auth = jwt_auth.authenticate(request)
        if user_auth is not None:
            return user_auth

        # Fallback to Session auth
        session_auth = SessionAuthentication()
        return session_auth.authenticate(request)

