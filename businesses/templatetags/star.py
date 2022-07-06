import math

from django import template

register = template.Library()


@register.filter
def full_star(value):
    return range(int(value))


@register.filter
def has_half_star(value):
    return int(value) != value


@register.filter
def empty_star(value):
    return range(5 - math.ceil(value))
