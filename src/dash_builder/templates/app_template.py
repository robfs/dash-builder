"""Module containing the template for app.py."""

from pathlib import Path

from typing_extensions import override

from ._base_template import BaseTemplate

__all__ = ["AppTemplate"]


class AppTemplate(BaseTemplate):
    """Template for building the app.py file."""

    path = Path("app.py")
    _dash_imports = ["html"]

    @staticmethod
    def app() -> str:
        """Get the string representation of the app."""
        args = ", ".join(
            ["__name__", "use_pages=True", "external_stylesheets=dmc.styles.ALL"]
        )
        lines: list[str] = [
            'dash._dash_renderer._set_react_version("18.2.0")',
            f"app: dash.Dash = dash.Dash({args})",
        ]
        return "\n".join(lines)

    @staticmethod
    def app_layout() -> str:
        """Get the string representation of the app layout."""
        return 'app.layout = html.Div([html.H1("This is the main application layout"), dash.page_container])'

    @staticmethod
    def main() -> str:
        """Get the string representation of the main function."""
        return 'if __name__ == "__main__":\n\tapp.run(debug=True)\n'

    @override
    @classmethod
    def content_list(cls) -> list[str]:
        return [cls.get_dash_imports(), cls.app(), cls.app_layout(), cls.main()]
