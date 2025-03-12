"""Pytest constants file."""

import pytest
from typer.testing import CliRunner

from src.dash_builder import DashPage, DashView


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def test_view() -> type[DashView]:
    class TestView(DashView):
        @classmethod
        def layout(cls, id: str, **kwargs):
            return []

    return TestView


@pytest.fixture()
def test_page() -> type[DashPage]:
    class TestPage(DashPage):
        @classmethod
        def valid_layout(cls, **kwargs):
            return []

    return TestPage


@pytest.fixture()
def error_page() -> type[DashPage]:
    class TestPage(DashPage):
        @classmethod
        def valid_layout(cls, **kwargs):
            return 1 / 0

    return TestPage
