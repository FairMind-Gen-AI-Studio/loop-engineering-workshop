"""AC3 · An unknown code is refused with ValueError."""
import unittest

import _base  # noqa: F401
from shop.cart import Cart
from shop.pricing import total


class UnknownCode(unittest.TestCase):
    def test_unknown_code_raises_value_error(self):
        cart = Cart(shipping=500).add("a", 10000)
        with self.assertRaises(ValueError):
            total(cart, code="NOPE")


if __name__ == "__main__":
    unittest.main()
