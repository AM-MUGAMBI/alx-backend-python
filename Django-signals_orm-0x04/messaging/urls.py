from django.urls import path
from .views import delete_user, home

urlpatterns = [
    path('', home, name='home'),  # This handles "/"
    path('delete_user/', delete_user, name='delete_user'),
]
