import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage

@pytest.mark.smoke
def test_smoke_search_pliers(page):
    """Goal: search products.
    Precondition: none.
    Expected: all displayed product names contain 'pliers'.
    """

    home = HomePage(page).open().search("pliers")

    # Chờ kết quả tìm kiếm hoàn tất
    expect(home.search_completed).to_be_visible()

    # Lấy danh sách tên sản phẩm
    names = home.product_names.all_text_contents()

    # Kiểm tra có sản phẩm
    assert len(names) > 0

    # Kiểm tra tất cả sản phẩm chứa "pliers"
    assert all("pliers" in name.lower() for name in names), names

@pytest.mark.smoke
def test_smoke_add_to_cart(page):
    """Goal: add three Claw Hammers to cart.
    Precondition: empty cart.
    Expected: cart badge shows 3.
    """

    product = HomePage(page).open().open_product("Claw Hammer")

    product.add_to_cart(quantity=3)

    expect(product.cart_quantity).to_have_text("3")

@pytest.mark.smoke
def test_smoke_invalid_login(page):
    """Goal: reject invalid credentials.
    Precondition: account does not exist.
    Expected: error message appears and URL remains /auth/login.
    """

    # Bước 1: Mở trang đăng nhập
    login = LoginPage(page).open()

    # Bước 2: Đăng nhập bằng email không tồn tại
    login.login(
        "nobody-here@example.com",
        "wrongpassword123"
    )

    # Bước 3: Kiểm tra thông báo lỗi
    expect(login.error).to_contain_text(
        "Invalid email or password"
    )

    # Bước 4: Kiểm tra URL
    expect(page).to_have_url(re.compile(r"/auth/login$"))


@pytest.mark.smoke
def test_smoke_empty_contact_form(page):
    """Goal: validate empty contact form.
    Precondition: all fields are empty.
    Expected: Subject and Message required errors appear.
    """

    # Bước 1: Mở trang Contact
    contact = ContactPage(page).open()

    # Bước 2: Nhấn Send khi chưa nhập dữ liệu
    contact.submit()

    # Bước 3: Kiểm tra lỗi Subject
    expect(
        contact.errors.filter(has_text="Subject is required")
    ).to_be_visible()

    # Bước 4: Kiểm tra lỗi Message
    expect(
        contact.errors.filter(has_text="Message is required")
    ).to_be_visible()