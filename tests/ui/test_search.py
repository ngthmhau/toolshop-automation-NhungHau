import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression

def test_search_keyword_without_results(page):
    home = HomePage(page)
    home.open()

    home.search("zzznothing999")

    expect(home.no_results).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_sort_products_by_price_ascending(page):
    home = HomePage(page)
    home.open()

    home.sort_by("price,asc")

    expect(home.sorting_completed).to_be_visible()

    prices = home.prices()

    assert len(prices) > 1, "Product list is empty or has only one product"
    assert prices == sorted(prices), (
        f"Products are not sorted by ascending price: {prices}"
    )
