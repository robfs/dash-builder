import pytest
from typer.testing import CliRunner

from src.dash_builder import DashView


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def test_view() -> type[DashView]:
    class TestView(DashView):
        @classmethod
        def create(cls, id: str, **kwargs):
            return []

    return TestView
