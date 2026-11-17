import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage


# ---------------------------------------------------------------- B1.1 (together with the teacher)
@pytest.mark.smoke
@pytest.mark.ui
def test_login_empty_form_shows_required_errors(page):
    """Goal: client-side validation.
    Precondition: none.
    Expected: 'Email is required' and 'Password is required'."""
    login = LoginPage(page).open()
    login.submit_button.click()
    expect(login.email_error).to_contain_text("Email is required")
    expect(login.password_error).to_contain_text("Password is required")