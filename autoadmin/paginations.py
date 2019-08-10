from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    # page_size_query_params = 'page_size'
    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get("page_size", -1))
            if page_size < 0:
                return self.page_size
            return page_size
        except:
            pass
        return self.page_size