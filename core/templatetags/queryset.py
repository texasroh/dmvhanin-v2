from django import template

register = template.Library()


@register.filter
def order_by(qs, args):
    args = [x.strip() for x in args.split(",")]
    return qs.order_by(*args)
