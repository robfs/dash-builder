"""Module containing a custom 404 error template."""

from pathlib import Path

from typing_extensions import override

from ._base_template import BaseTemplate

__all__ = ["NotFound404Template"]


class NotFound404Template(BaseTemplate):
    path = Path("pages") / "not_found_404.py"
    _dash_imports = ["html"]
    _dash_builder_imports = ["DashPage"]

    @override
    @classmethod
    def content_list(cls) -> list[str]:
        style = '{"margin": "auto", "display": "flex"}'
        image_url = (
            "https://img.freepik.com/free-vector/hand-drawn-404-error_23-2147746234.jpg"
        )
        layout = f'[html.Img(src="{image_url}", style={style})]'
        return list(cls.get_default_page_contents(layout=layout))
