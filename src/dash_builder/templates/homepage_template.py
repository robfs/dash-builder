"""Module containing the home page template."""

from pathlib import Path

from typing_extensions import override

from ._base_template import BaseTemplate

__all__ = ["HomepageTemplate"]


class HomepageTemplate(BaseTemplate):
    """Template for building the hompeage home.py file."""

    path = Path("pages") / "home.py"
    _dash_imports = ["html"]
    _dash_builder_imports = ["DashPage"]

    @override
    @classmethod
    def content_list(cls) -> list[str]:
        layout = '[html.H2("This is the page layout")]'
        return list(cls.get_default_page_contents(path="/", layout=layout))
