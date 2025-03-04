"""Module containing the abstract DashView class for defining components of application pages."""

import abc
import re
import typing

from dash import ALL, MATCH
from dash.dependencies import _Wildcard

__all__ = ["DashView"]

PASCAL_TO_SNAKE_REGEX = re.compile(r"(?<!^)(?=[A-Z])")


class ComponentId(typing.TypedDict):
    type: str
    index: str | _Wildcard


class DashView(abc.ABC):
    @staticmethod
    def _convert_camel_to_snake_case(input: str) -> str:
        return PASCAL_TO_SNAKE_REGEX.sub("-", input).lower()

    @classmethod
    def name(cls, subname: str | None = None) -> str:
        n: str = cls._convert_camel_to_snake_case(cls.__name__)
        if subname is not None:
            n += f"-{subname}"
        return n

    @classmethod
    def id(cls, id: str | _Wildcard, subname: str | None = None) -> ComponentId:
        return ComponentId(type=cls.name(subname), index=id)

    @classmethod
    def matched_id(cls) -> ComponentId:
        return cls.id(MATCH)

    @classmethod
    def all_ids(cls) -> ComponentId:
        return cls.id(ALL)

    @classmethod
    @abc.abstractmethod
    def create(cls, id: str, **kwargs):
        raise NotImplementedError
