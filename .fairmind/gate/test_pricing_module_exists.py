"""A check written badly on purpose: it passes before any work is done.

It asserts that shop/pricing.py exists, which was already true when the task
started. A check that has never been red has never proved anything, so admission
refuses it and puts it in quarantine. No acceptance criterion points at it.
"""
import os
import unittest

import _base


class PricingModuleExists(unittest.TestCase):
    def test_pricing_module_exists(self):
        self.assertTrue(os.path.exists(os.path.join(_base.ROOT, "shop", "pricing.py")))


if __name__ == "__main__":
    unittest.main()
