from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import Message


def get_threaded_replies(message):
    """
    Recursive function to get replies in a threaded way.
    Each message includes its children replies.
    """
    replies = Message.objects.filter(parent_message=message).select_related('sender', 'receiver')
    thread = []
    for reply in replies:
        thread.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return thread


@login_required
def user_messages(request):
    """
    View to display all messages for a user, with threaded replies.
    Using select_related and prefetch_related to optimize queries.
    """
    # Get top-level messages where user is sender and no parent message (root messages)
    messages = Message.objects.filter(
        sender=request.user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver')

    # Build threaded message structure
    threaded_messages = []
    for msg in messages:
        threaded_messages.append({
            'message': msg,
            'replies': get_threaded_replies(msg)
        })

    return render(request, 'messaging/messages.html', {
        'threaded_messages': threaded_messages
    })


def home(request):
    return HttpResponse("""
        <html>
        <head>
            <style>
                body {
                    display: flex;
                    flex-direction: column;
                    margin: 0;
                    height: 100vh;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: navy;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin: 20px 0 0 0;
                }
                .center-content {
                    flex-grow: 1;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                }
                h2 {
                    margin: 10px 0;
                    color: red;
                }
                a {
                    color: navy;
                    text-decoration: none;
                    font-weight: bold;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1><u>Welcome to the Messaging App</u></h1>
            <div class="center-content">
                <h2>to continue, please use</h2>
                <h2><a href="/admin/">admin panel</a></h2>
            </div>
        </body>
        </html>
    """)


@require_POST
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('/')  # Redirect to home page after deletion
