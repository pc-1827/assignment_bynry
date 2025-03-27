from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replaces all instances of the first argument with the second argument in the given string.
    """
    if len(arg.split(',')) > 1:
        old, new = arg.split(',', 1)
        return value.replace(old, new)
    return value.replace(arg, ' ')