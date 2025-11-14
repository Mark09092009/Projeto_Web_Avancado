from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    try:
        if len(arg.split(':')) != 2:
            return value 
        
        old, new = arg.split(':')
        return str(value).replace(old, new)
    except Exception:
        return value