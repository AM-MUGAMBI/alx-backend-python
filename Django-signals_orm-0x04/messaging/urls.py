from django.urls import path
from .views import delete_user, home, user_messages

urlpatterns = [
    path('', home, name='home'),
    path('messages/', user_messages, name='user_messages'),
    path('delete_user/', delete_user, name='delete_user'),
]

