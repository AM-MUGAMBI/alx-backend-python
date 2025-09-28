# chats/middleware.py

from datetime import datetime
import logging
import os

# Set up logging to file
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../requests.log')
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response

