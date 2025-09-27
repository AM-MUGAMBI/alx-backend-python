from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Pagination class that returns 20 messages per page by default.
    Allows client to override page size up to a maximum of 100.
    """
    page_size = 20
    page_size_query_param = 'page_size'  # Optional: allow client to override page size
    max_page_size = 100
