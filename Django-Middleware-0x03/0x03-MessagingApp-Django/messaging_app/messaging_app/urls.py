from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Main API routes for the chats app
    path('api/', include('chats.urls')),

    # JWT Authentication endpoints
    # POST: obtain access and refresh tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # POST: refresh access token using a valid refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # DRF's built-in login/logout views for the browsable API
    path('api-auth/', include('rest_framework.urls')),
]
