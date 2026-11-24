from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage

scenarios("search.feature")


@given("I open the Toolshop home page", target_fixture="home")
def open_home(page):
    return HomePage(page).open()


@when(parsers.parse('I search for "{keyword}"'))
def search(home, keyword):
    home.search(keyword)


@then("I see the no-results message")
def check_no_results(home):
    expect(home.no_results).to_be_visible()