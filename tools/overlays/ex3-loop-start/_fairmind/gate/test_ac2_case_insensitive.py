"""AC2 · Codes are case-insensitive."""
import unittest

import _base  # noqa: F401
from shop.cart import Cart
from shop.pricing import total


class CaseInsensitive(unittest.TestCase):
    def test_lowercase_code_matches(self):
        cart = Cart(shipping=500).add("a", 10000)
        self.assertEqual(total(cart, code="save10"), total(cart, code="SAVE10"))
        self.assertLess(total(cart, code="save10"), total(cart))


if __name__ == "__main__":
    unittest.main()
