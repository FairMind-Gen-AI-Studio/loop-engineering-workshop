from shop.cart import Cart
from shop.pricing import shipping_for


def test_large_order_ships_free():
    assert shipping_for(Cart(shipping=590).add("a", 6000)) == 0


def test_small_order_pays_shipping():
    assert shipping_for(Cart(shipping=590).add("a", 4000)) == 590


def test_exactly_the_threshold_ships_free():
    assert shipping_for(Cart(shipping=590).add("a", 5000)) == 0


def test_receipt_shows_the_shipping_charged():
    from shop.receipt import money, render
    lines = render(Cart(shipping=590).add("a", 6000)).splitlines()
    shipping_line = next(line for line in lines if line.startswith("shipping"))
    assert shipping_line.endswith(money(0))
