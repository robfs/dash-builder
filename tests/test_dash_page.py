"""Tests for the DashPage class."""

import pytest
from dash import html

from src.dash_builder import DashPage


def test_page_error(test_page):
    container = test_page.error_container("test message")
    inner = container.children
    inner_text = inner.children
    assert isinstance(container, html.Div)
    assert isinstance(inner, html.Pre)
    assert inner_text == "test message"


def test_page_on_error(error_page):
    container = error_page.layout()
    inner = container.children
    inner_text = inner.children
    assert isinstance(container, html.Div)
    assert isinstance(inner, html.Pre)
    assert "ZeroDivisionError: division by zero" in inner_text


def test_abstract_page_raises():
    with pytest.raises(TypeError):
        DashPage()


def test_abstract_valid_layout_raises():
    with pytest.raises(NotImplementedError):
        DashPage.valid_layout()
