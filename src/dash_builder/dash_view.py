"""Module containing the abstract DashView class for defining components of application pages."""

import abc
import re
import typing

from dash import ALL, MATCH
from dash.dependencies import _Wildcard

__all__ = ["DashView", "ComponentId"]

PASCAL_TO_SNAKE_REGEX = re.compile(r"(?<!^)(?=[A-Z])")


class ComponentId(typing.TypedDict):
    """Dictionary class for component IDs."""

    type: str
    """`type` field of component IDs. Uses an encoded version of the view name / subname."""
    index: str | _Wildcard
    """`index` field of component IDs. User value allows for logical management of components within and across views and pages."""


class DashView(abc.ABC):
    """Abstract class for defining views in a Dash application.

    Views are single, or groups of, components that make up the application interface.
    """

    @staticmethod
    def _convert_camel_to_snake_case(input: str) -> str:
        """Convert camel case string to snake case.

        Args:
            input: camel case formatted text to convert.

        Returns:
            snake case formatted text.

        """
        return PASCAL_TO_SNAKE_REGEX.sub("-", input).lower()

    @classmethod
    def name(cls, subname: str | None = None) -> str:
        """View name, used as the `type` field of component IDs.

        Args:
            subname: string to append to the class name.

        Returns:
            string of the view name.

        """
        n: str = cls._convert_camel_to_snake_case(cls.__name__)
        if subname is not None:
            n += f"-{subname}"
        return n

    @classmethod
    def id(cls, id: str | _Wildcard, subname: str | None = None) -> ComponentId:
        """Generate unique component ID to link callbacks between views.

        Equivalent to

        ```python
        {"type": cls.name(subname), "index": id}
        ```

        Args:
            id: logical identifier for the component.
            subname: string to append to the class name.

        Returns:
            `ComponentId` dictionary of the component ID.

        """
        return ComponentId(type=cls.name(subname), index=id)

    @classmethod
    def matched_id(cls) -> ComponentId:
        """Generate a matching callback ID for the view.

        Equivalent to

        ```python
        {"type": cls.name(subname), "index": dash.MATCH}
        ```

        """
        return cls.id(MATCH)

    @classmethod
    def all_ids(cls) -> ComponentId:
        """Generate an all index matching callback ID for the view.

        Equivalent to

        ```python
        {"type": cls.name(subname), "index": dash.ALL}
        ```

        """
        return cls.id(ALL)

    @classmethod
    @abc.abstractmethod
    def layout(cls, id: str, **kwargs):
        """Create the components of the view.

        Arguments:
            id: logical identifier for the component.
            **kwargs: additional keyword arguments.

        Raises:
            `NotImplementedError`: must be implemented by the subclass.

        """
        raise NotImplementedError
