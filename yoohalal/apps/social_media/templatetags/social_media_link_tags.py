from django import template
from apps.social_media.models import LinkType
register = template.Library()

@register.assignment_tag
def get_social_media_links(limit=False, randomize=False):
	qs = LinkType.objects.filter(is_visible=True).order_by('order_number')

	if randomize:
		qs = qs.order_by('?')

	if limit:
		qs = qs[0:limit]
		
	return qs