from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name="currency")
def currency(value):
    try:
        value = Decimal(value)
        print(value, f"<span>{value:.2f}</span>$")
        return f"<span>{value:.2f}</span>$"
    except (ValueError, TypeError):
        return value