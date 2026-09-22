from shop.receipt import money


def test_money_always_shows_two_decimals():
    assert money(2450) == "24.50 EUR"
    assert money(711) == "7.11 EUR"
    assert money(5) == "0.05 EUR"
