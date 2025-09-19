from django.urls import path, include
from rest_framework import routers  # Import routers from rest_framework
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()  # Create a DefaultRouter instance
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]

