from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    
    max_limit = 10


class PostPageNumberPagination(PageNumberPagination):
	page_size = 12
	def get_paginated_response(self, data):
		response = super(PostPageNumberPagination, self).get_paginated_response(data)
		response.data['total_pages'] = self.page.paginator.num_pages
		response.data['current'] = self.page.number
		return response