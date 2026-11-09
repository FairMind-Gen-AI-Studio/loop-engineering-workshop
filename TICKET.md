# DISC-1 · Discount codes at checkout

Customers can enter a discount code at checkout.

- `SAVE10` takes 10% off.
- `FREE100` takes 100% off.
- Codes are case-insensitive.
- An unknown code is refused with an error.

`shop.pricing.total(cart, code=None)` takes the code. Without a code, totals do not change.
