from django import template
register = template.Library()

@register.simple_tag
def pokemon(obj,method,ids):
	method = getattr(obj, method, default)
	return method.get(email_data=ids)
