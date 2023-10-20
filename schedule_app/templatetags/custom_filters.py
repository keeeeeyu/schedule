from django import template

register = template.Library()

@register.filter(name='hours_range')
def hours_range(start, end):

    return range(start, end)