from rest_framework.pagination import CursorPagination

class MyCursorPagination(CursorPagination):
    page_sixe = 15
    ordering = 'title'
    cursor_query_param = 'cu'