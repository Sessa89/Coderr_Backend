from rest_framework.pagination import PageNumberPagination

class OfferPagination(PageNumberPagination):
    """
    Pagination class for Offer listings.

    Attributes:
        page_size_query_param (str): Query parameter name for clients to
            specify page size.
        page_size (int): Default number of items per page.
    """
    page_size_query_param = 'page_size'
    page_size = 6