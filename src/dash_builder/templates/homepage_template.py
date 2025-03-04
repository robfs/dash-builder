"""Module containing the home page template."""

from pathlib import Path

from ._base_template import BaseTemplate

__all__ = ["HomepageTemplate"]


class HomepageTemplate(BaseTemplate):
    path = Path("pages") / "home.py"
    _dash_imports = ["html"]
    _dash_builder_imports = ["DashPage"]

    @classmethod
    def content_list(cls) -> list[str]:
        layout = '[html.H1("This is the Homepage")]'
        return list(cls.page_default_contents(path="/", layout=layout))
