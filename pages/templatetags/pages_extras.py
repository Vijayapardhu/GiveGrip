from django import template

register = template.Library()

@register.filter
def times(value):
    """Return a range of numbers from 1 to value."""
    return range(1, int(value) + 1)
