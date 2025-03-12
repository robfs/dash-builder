"""Module containing the template for a new page."""

from pathlib import Path

from .object_template import ObjectTemplate

__all__ = ["PageTemplate"]


class PageTemplate(ObjectTemplate):
    """Template for a new page."""

    _type = "Page"

    def __init__(self, page_name: str, page_path: Path, url_path: str | None = None):
        """Initialise the PageTemplate."""
        super().__init__(page_name, page_path)
        self.url_path: str | None = url_path

    @property
    def class_comment(self) -> str:
        """Get the class comment of the page."""
        return f'"""{self.class_name}."""'

    @property
    def imports(self) -> str:
        """Get the imports of the page."""
        return "\n".join(
            [
                "import dash",
                "import dash_mantine_components as dmc",
                "from dash import html",
                "from dash_builder import DashPage\n\n",
            ]
        )

    @property
    def page_registration(self) -> str:
        """Get the page registration of the page."""
        if self.url_path is None:
            return "dash.register_page(__name__)\n\n"
        return f'dash.register_page(__name__, path="{self.url_path}")\n\n'

    @property
    def class_definition(self) -> str:
        """Get the class definition of the page."""
        return "\n".join(
            [
                f"class {self.class_name}(DashPage):",
                f"\t{self.class_comment}\n",
                "\t@classmethod",
                "\tdef valid_layout(cls, **kwargs):",
                f'\t\t"""Render valid layout for the {self.class_name}."""',
                f'\t\treturn [html.Div(dmc.Title("This is the {self.class_name}", order=2))]\n',
            ]
        )

    @property
    def layout_definition(self) -> str:
        """Get the layout definition of the page."""
        return "\n".join(
            [
                "\ndef layout(**kwargs):",
                f'\t"""Render valid layout for the {self.class_name}."""',
                f"\treturn {self.class_name}.layout(**kwargs)\n",
            ]
        )

    @property
    def file_content(self) -> str:
        """Get the file content of the page."""
        return "\n".join(
            [
                self.module_comment,
                self.imports,
                self.page_registration,
                self.class_definition,
                self.layout_definition,
            ]
        )
