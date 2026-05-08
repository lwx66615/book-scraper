import pytest
from app.crawlers.adapters import get_adapter_for_site
from app.crawlers.adapters.example_adapter import ExampleSiteAdapter


def test_get_adapter_for_site():
    adapter_class = get_adapter_for_site("example.com")
    assert adapter_class == ExampleSiteAdapter

    unknown_adapter = get_adapter_for_site("unknown.com")
    assert unknown_adapter is None


def test_example_adapter_init():
    adapter = ExampleSiteAdapter()
    assert adapter.selectors is not None
    assert "book_title" in adapter.selectors
