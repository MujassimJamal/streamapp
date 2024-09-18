from django import template

register = template.Library()

@register.filter
def index(array, i):
    try:
        return array[i]
    except:
        return ''
