"""Module containing the template for app.py."""

from pathlib import Path

from typing_extensions import override

from ._base_template import BaseTemplate

__all__ = ["AppTemplate"]


class AppTemplate(BaseTemplate):
    """Template for building the app.py file."""

    path = Path("app.py")
    _dash_imports = ["html"]
    _dash_builder_imports = ["DashPage"]

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
        return "\n\n".join(lines)

    @staticmethod
    def app_header() -> str:
        """Get the header bar / navbar for the app."""
        return 'dmc.AppShellHeader("")'

    @staticmethod
    def app_navbar() -> str:
        """Get the sidebar / navbar for the app."""
        return 'dmc.AppShellNavbar("")'

    @staticmethod
    def app_main() -> str:
        """Get the main content for the app."""
        return "dmc.AppShellMain(dash.page_container)"

    @staticmethod
    def app_aside() -> str:
        """Get the sidebar / navbar for the app."""
        return 'dmc.AppShellAside("")'

    @staticmethod
    def app_footer() -> str:
        """Get the footer for the app."""
        return 'dmc.AppShellFooter("")'

    @classmethod
    def app_shell(cls) -> str:
        """Get the string representation of the app shell."""
        header = cls.app_header()
        navbar = cls.app_navbar()
        main = cls.app_main()
        aside = cls.app_aside()
        footer = cls.app_footer()
        components = "[" + ",".join([header, navbar, main, aside, footer]) + "]"
        return f"dmc.AppShell({components})"

    @classmethod
    def app_layout(cls) -> str:
        """Get the string representation of the app layout."""
        return f"dmc.MantineProvider({cls.app_shell()})"

    @classmethod
    def get_app_layout_definition(cls) -> str:
        """Get the string representation of the app layout definition."""
        return f"app.layout = {cls.get_page_name()}.layout()"

    @staticmethod
    def get_main_function() -> str:
        """Get the string representation of the main function."""
        return 'if __name__ == "__main__":\n\tapp.run(debug=True)'

    @override
    @classmethod
    def content_list(cls) -> list[str]:
        return [
            cls.get_dash_imports(),
            cls.get_dash_builder_imports(),
            cls.app(),
            cls.get_page_class(cls.app_layout()),
            cls.get_app_layout_definition(),
            cls.get_main_function(),
        ]
