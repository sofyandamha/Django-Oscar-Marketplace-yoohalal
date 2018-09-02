from oscar.core.loading import get_class
from django.conf import settings

SearchForm = get_class('search.forms', 'SearchForm')

def search_form(request):
    """
    Ensure that the search form is available site wide
    """
    return {'search_form': SearchForm(request.GET),
    'OSCAR_FROM_EMAIL' : settings.OSCAR_FROM_EMAIL,
    'EMAIL_HOST_USER' : settings.EMAIL_HOST_USER}