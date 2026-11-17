import json
from pathlib import Path

import pytest

from conftest import new_email, register_user, strong_password  # noqa: F401  (you will need them)

KEYWORDS = json.loads((Path(__file__).parents[2] / "data" / "search_keywords.json").read_text())


# ---------------------------------------------------------------- B2.1 (together)
@pytest.mark.smoke
@pytest.mark.api
# ---------------------------------------------------------------- B2.2
def test_products_first_page_has_pagination_and_product_shape(api):
    """Goal: contract of GET /products.
    Precondition: none.
    Expected: keys current_page/data/per_page/total/last_page, 0 < len(data) <= per_page,
    every product has id (str or int), a non-empty name and a price > 0.
    Rule: NO absolute numbers (PROD has 50 products, BUGGY 26)."""
    response = api.get("/products", params={"page": 1})
    assert response.status == 200, response.text()
    body = response.json()
    for key in ("current_page", "data", "per_page", "total", "last_page"):
        assert key in body, f"missing key {key}"
    assert 0 < len(body["data"]) <= body["per_page"]
    for product in body["data"]:
        assert isinstance(product["id"], (str, int))
        assert isinstance(product["name"], str) and product["name"].strip()
        assert isinstance(product["price"], (int, float)) and product["price"] > 0


# ---------------------------------------------------------------- B2.3 data-driven
@pytest.mark.api
@pytest.mark.parametrize("case", KEYWORDS, ids=[c["keyword"] for c in KEYWORDS])
def test_search_api_returns_only_matching_names(api, case):
    """Goal: GET /products/search?q=... filters by name.
    Precondition: none.
    Expected: at least one result and every name contains the keyword.
    Extra: add "saw" and "wrench" to data/search_keywords.json - no code change needed."""
    response = api.get("/products/search", params={"q": case["keyword"]})
    assert response.status == 200, response.text()
    names = [p["name"] for p in response.json()["data"]]
    assert names, f"no results for {case['keyword']}"
    assert all(case["must_contain"] in n.lower() for n in names), names


# ---------------------------------------------------------------- B2.4 errors
@pytest.mark.api
@pytest.mark.parametrize("path, expected", [("/users/me", 401), ("/products/does-not-exist", 404)])
def test_protected_or_missing_resource_returns_4xx(api, path, expected):
    """Goal: error handling. Precondition: no token.
    Expected: 401 for a protected resource, 404 for a missing one."""
    response = api.get(path)
    assert response.status == expected, response.text()