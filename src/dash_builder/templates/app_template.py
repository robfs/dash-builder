"""Module containing the template for app.py."""

from pathlib import Path

from typing_extensions import override

from ._base_template import BaseTemplate

__all__ = ["AppTemplate"]


class AppTemplate(BaseTemplate):
    """Template for building the app.py file."""

    path = Path("app.py")

    @staticmethod
    def app() -> str:
        """Get the string representation of the app."""
        return "app: dash.Dash = dash.Dash(__name__, use_pages=True)"

    @staticmethod
    def main() -> str:
        """Get the string representation of the main function."""
        return 'if __name__ == "__main__":\n\tapp.run(debug=True)\n'

    @override
    @classmethod
    def content_list(cls) -> list[str]:
        return [cls.get_dash_imports(), cls.app(), cls.main()]
