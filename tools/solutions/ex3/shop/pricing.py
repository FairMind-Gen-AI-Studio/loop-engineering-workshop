"""What a cart costs.

VAT applies to the items only. Shipping is a flat fee, added after VAT and never
taxed. Every rule about money that is not a tax lives here.
"""

from decimal import ROUND_HALF_UP, Decimal

from .cart import Cart
from .tax import vat

DISCOUNT_CODES = {"SAVE10": 10, "FREE100": 100}  # percent off the items


def discount(items: int, code) -> int:
    """Cents taken off the items for `code`. Shipping is never discounted."""
    if code is None:
        return 0
    try:
        percent = DISCOUNT_CODES[code.upper()]
    except KeyError:
        raise ValueError(f"unknown discount code {code!r}") from None
    return int((Decimal(items) * percent / 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def total(cart: Cart, code=None) -> int:
    """Discounted items, plus VAT on them, plus shipping. In cents."""
    items = cart.subtotal() - discount(cart.subtotal(), code)
    return items + vat(items) + cart.shipping
