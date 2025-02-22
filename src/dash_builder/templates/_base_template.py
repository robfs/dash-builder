"""Module containing the base template for generating project files."""

import abc

__all__ = ["BaseTemplate"]


class BaseTemplate(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def content_list(cls) -> list[str]:
        raise NotImplementedError

    @classmethod
    def content(cls) -> str:
        return "\n\n".join(cls.content_list())
