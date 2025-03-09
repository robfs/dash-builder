"""Module containing the abstract DashView class for defining components of application pages."""

import abc
import typing

from dash import ALL, MATCH
from dash.dependencies import _Wildcard
from typing_extensions import override

from ._dash_object import DashObject

__all__ = ["DashView", "ComponentId"]


class ComponentId(typing.TypedDict):
    """Dictionary class for component IDs."""

    type: str
    """`type` field of component IDs. Uses an encoded version of the view name / subname."""
    index: str | _Wildcard
    """`index` field of component IDs. User value allows for logical management of components within and across views and pages."""


class DashView(DashObject):
    """Abstract class for defining views in a Dash application.

    Views are single, or groups of, components that make up the application interface.
    """

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

    @override
    @classmethod
    @abc.abstractmethod
    def valid_layout(cls, id: str, **kwargs):
        """Generate the desired page layout.

        Args:
            id: logical identifier for the component.
            kwargs: additional keyword arguments.

        Raises:
            `NotImplementedError`: must be implemented by the subclass.

        """
        raise NotImplementedError
