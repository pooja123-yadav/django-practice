from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage, Page


def get_paginated_response(queryset, page=1, limit=10, paginator_cls=Paginator):
    result = {"paginator_details": {}}
    paginator = paginator_cls(queryset, limit)

    try:
        paginator_obj = paginator.page(page)

    except PageNotAnInteger:
        paginator_obj = paginator.page(1)

    except EmptyPage:
        paginator_obj = paginator.page(paginator.num_pages)

    result["paginator_details"]["num_of_pages"] = paginator.num_pages
    result["paginator_details"]["current_page"] = paginator_obj.number
    result["object_list"] = paginator_obj.object_list
    return result


# class DSEPaginator(Paginator):
#     def __init__(self, *args, **kwargs):
#         super(DSEPaginator, self).__init__(*args, **kwargs)
#         setattr(self, 'count', self.object_list.count())
#         self.object_list = [hit.to_dict() for hit in self.object_list]

#     def page(self, number):
#         # this is overridden to prevent any slicing of the object_list - Elasticsearch has
#         # returned the sliced data already.
#         number = self.validate_number(number)
#         return Page(self.object_list, number, self)