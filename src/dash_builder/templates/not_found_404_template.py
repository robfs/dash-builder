"""Module containing a custom 404 error template."""

from ._base_template import BaseTemplate

__all__ = ["NotFound404Template"]


class NotFound404Template(BaseTemplate):
    _dash_builder_imports = ["DashPage"]

    @classmethod
    def content_list(cls) -> list[str]:
        return list(cls.page_default_contents())
