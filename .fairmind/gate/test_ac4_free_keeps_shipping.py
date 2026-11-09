"""AC4 · FREE100 makes the items free; shipping is still charged."""
import unittest

import _base  # noqa: F401
from shop.cart import Cart
from shop.pricing import total


class FreeKeepsShipping(unittest.TestCase):
    def test_free100_still_charges_shipping(self):
        cart = Cart(shipping=700).add("a", 5000)
        self.assertEqual(total(cart, code="FREE100"), 700)


if __name__ == "__main__":
    unittest.main()
