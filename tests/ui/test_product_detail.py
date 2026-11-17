import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_product_detail_displays_correct_name_and_price(page):
    home = HomePage(page)
    home.open()

    product = home.open_product("Hammer")

    # Kiểm tra tên sản phẩm
    expect(product.name).to_be_visible()
    assert product.get_name() == "Hammer"

    # Kiểm tra giá sản phẩm
    expect(product.unit_price).to_be_visible()

    price = product.price()
    assert price > 0
