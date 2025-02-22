"""Module containing the home page template."""

from ._base_template import BaseTemplate

__all__ = ["HomepageTemplate"]


class HomepageTemplate(BaseTemplate):
    @classmethod
    def content_list(cls) -> list[str]:
        return [cls.page_imports()]
