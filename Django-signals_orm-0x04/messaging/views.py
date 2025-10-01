from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


@require_POST
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('/')  # Redirect to home or login page after deletion
