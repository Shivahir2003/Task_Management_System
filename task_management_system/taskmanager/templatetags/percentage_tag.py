from django import template

register = template.Library()

@register.filter
def as_percentage_of(part, whole):
    try:
        return "%d%%" % (float(part) / whole * 100)
    except (ValueError, ZeroDivisionError):
        return ""

@register.filter
def percentage(part, whole):
    try:
        return round(float(part) / whole * 100)
    except (ValueError, ZeroDivisionError):
        return ""
