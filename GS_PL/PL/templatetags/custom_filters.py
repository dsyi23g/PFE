from django import template

register = template.Library()

@register.filter
def until(value, end):
    return range(value, end)
