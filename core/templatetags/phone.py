import re

from django import template

register = template.Library()


@register.filter
def phone(value):
    value = re.sub(r"[^0-9]", "", value)
    if len(value) == 10:
        return value[:3] + "-" + value[3:6] + "-" + value[6:]
    return value
