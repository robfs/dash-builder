"""Module containing the home page template."""

from ._base_template import BaseTemplate

__all__ = ["HomepageTemplate"]


class HomepageTemplate(BaseTemplate):
    _dash_builder_imports = ["DashPage"]

    @classmethod
    def content_list(cls) -> list[str]:
        imports, register, page, layout = cls.page_default_contents()
        return [imports, register, page, layout]
