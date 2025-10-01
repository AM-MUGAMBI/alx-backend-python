from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse


@require_POST
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('/')



def home(request):
    return HttpResponse("""
        <html>
        <head>
            <style>
                body {
                    margin: 0;
                    background-color: #f5f5f5;
                    font-family: Arial, sans-serif;
                }

                header {
                    text-align: center;
                    padding: 20px;
                }

                h1 {
                    color: navy;
                    margin: 0;
                }

                main {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: calc(100vh - 80px);  /* Full height minus header */
                    text-align: center;
                    flex-direction: column;
                }

                h2 a {
                    text-decoration: none;
                    color: navy;
                }

                h2 a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Welcome to the Messaging App</h1>
            </header>
            <main>
                <h2>To continue, please use</h2><br>
                <h2><a href="/admin/">Admin Panel</a></h2>
            </main>
        </body>
        </html>
    """)

