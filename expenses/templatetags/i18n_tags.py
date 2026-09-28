from decimal import Decimal, InvalidOperation

from django import template

from expenses.translations import DEFAULT_LANGUAGE, translate

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, key, **kwargs):
    """{% t "key" %}  or  {% t "remaining" amount=value %}"""
    return translate(key, context.get("LANG", DEFAULT_LANGUAGE), **kwargs)


def _to_decimal(value):
    try:
        return Decimal(str(value if value not in (None, "") else 0))
    except (InvalidOperation, ValueError):
        return None


@register.filter
def money(value):
    """5000 -> '5,000.00' (same look in every language)."""
    number = _to_decimal(value)
    return value if number is None else f"{number:,.2f}"


@register.filter
def num(value):
    """5000 -> '5000.00' (safe for <input type="number" value="...">)."""
    number = _to_decimal(value)
    return "" if number is None else f"{number:.2f}"
