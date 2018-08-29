from django import template

register = template.Library()

@register.filter
def circle(cur, pg):
    offset = abs(cur - pg)
    if offset < 3:
        return True
    return False