from django.conf import settings

from oscar.apps.catalogue.search_handlers import SimpleProductSearchHandler


class SimpleProductSearchHandler(SimpleProductSearchHandler):

    def get_queryset(self):
        return super(SimpleProductSearchHandler, self).get_queryset().filter(status='publish')