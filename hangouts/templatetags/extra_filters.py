from django import template

register = template.Library()

@register.filter()
def keys(dict):
	return dict.keys()


@register.filter
def max_list(l):
	return max(l)

@register.filter
def min_list(l):
	return min(l)


