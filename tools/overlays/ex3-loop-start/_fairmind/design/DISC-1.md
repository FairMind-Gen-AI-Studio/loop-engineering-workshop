# DISC-1 · Design brief

## 1. The problem, in the code's own terms

`shop.pricing.total(cart)` returns items plus VAT on the items plus shipping. The ticket
adds an optional `code` argument that takes a percentage off. The ticket says what the
codes are; it does not say what the percentage is taken off.

## 2. Where each invariant lives

The discount is a rule about money that is not a tax, so it lives in `shop/pricing.py`,
next to `total`, which is where the module docstring puts every such rule. It applies to
**the items only**, before VAT: VAT is then computed on the discounted items. **Shipping is
never discounted**: it is a flat fee added after VAT, exactly as today. So `FREE100` makes
the items free and the order still costs its shipping. A total can therefore never go
below the shipping fee, and never below zero. `receipt.render` calls `total`, so it follows
without a change; no other caller computes a total.

## 3. Refusal and error semantics

An unknown code raises `ValueError`, the same class `Cart.add` raises for an invalid
item: it is bad input from the caller, not a failure of the shop.

## 4. The precedent, and where it stops

VAT already applies to items only and never to shipping; the discount follows that
precedent. Rounding follows `shop.tax.vat`: half up, to the cent, on integers.

## 5. Non-happy inputs

`code=None` means no discount. Lowercase and mixed-case codes match. An empty string is an
unknown code.

## 6. Out of scope

Stacking several codes, fixed-amount codes, expiry dates, and showing the discount on the
receipt.
