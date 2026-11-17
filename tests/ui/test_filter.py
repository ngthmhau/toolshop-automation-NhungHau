
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_filter_products_by_hammer_category(page):
    home = HomePage(page)
    home.open()

    home.filter_by_hammer()

    expect(home.product_names.first).to_be_visible()
