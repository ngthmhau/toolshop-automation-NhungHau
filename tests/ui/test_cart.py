import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
@pytest.mark.smoke
@pytest.mark.ui

def test_cart_line_price_equals_unit_price_times_quantity(page):
    """Goal: cart arithmetic.
    Precondition: empty cart (a new context per test gives you one).
    Expected: line price = unit price x 2 and total = sum of the lines."""
    product = HomePage(page).open().open_product("Combination Pliers")
    unit = product.price()
    product.add_to_cart(quantity=2)
    expect(product.cart_quantity).to_have_text("2")
    cart = product.go_to_cart()
    expect(cart.product_titles).to_have_count(1)
    assert cart.line_totals() == [pytest.approx(unit * 2)]
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))

@pytest.mark.ui
def test_cart_continue_shopping_returns_to_home(page):
    """Goal: page objects chain: each action returns the next page object.
    Precondition: none.
    Expected: after 'Continue Shopping' the product grid is visible again."""
    cart = HomePage(page).open().open_product("Hammer").add_to_cart().go_to_cart()
    expect(cart.product_titles.first).to_have_text("Hammer")
    cart.continue_shopping.click()
    expect(HomePage(page).product_names.first).to_be_visible()
