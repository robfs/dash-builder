"""Module containing the home page template."""

from pathlib import Path

from typing_extensions import override

from ._base_template import BaseTemplate

__all__ = ["HomepageTemplate"]


class HomepageTemplate(BaseTemplate):
    path = Path("pages") / "home.py"
    _dash_imports = ["html"]
    _dash_builder_imports = ["DashPage"]

    @override
    @classmethod
    def content_list(cls) -> list[str]:
        layout = '[html.H1("This is the Homepage")]'
        return list(cls.get_default_page_contents(path="/", layout=layout))
