"""AC1 · SAVE10 takes 10% off the items; VAT is computed on the discounted items."""
import unittest

import _base  # noqa: F401
from shop.cart import Cart
from shop.pricing import total


class PercentOff(unittest.TestCase):
    def test_save10_takes_ten_percent_off_the_items(self):
        cart = Cart(shipping=500).add("a", 10000)
        # items 10000 - 1000 = 9000; VAT 22% of 9000 = 1980; shipping 500
        self.assertEqual(total(cart, code="SAVE10"), 9000 + 1980 + 500)


if __name__ == "__main__":
    unittest.main()
