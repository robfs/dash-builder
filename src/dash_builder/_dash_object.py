"""Module containing the basic DashObject class for creating Dash objects."""

import abc
import re
import traceback

from dash import html

__all__ = ["DashObject"]

PASCAL_TO_KEBAB_REGEX = re.compile(r"(?<!^)(?=[A-Z])")


class DashObject(abc.ABC):
    """Abstract base class for creating Dash objects."""

    @staticmethod
    def _convert_pascal_to_kebab_case(input: str) -> str:
        """Convert PascalCaseString to kebab-case-string.

        Args:
            input: PascalCase formatted text to convert.

        Returns:
            kebab-case formatted text.

        """
        return PASCAL_TO_KEBAB_REGEX.sub("-", input).lower()

    @classmethod
    def name(cls, subname: str | None = None) -> str:
        """View name, used as the `type` field of component IDs.

        Args:
            subname: string to append to the class name.

        Returns:
            string of the view name.

        """
        n: str = cls._convert_pascal_to_kebab_case(cls.__name__)
        if subname is not None:
            n += f"-{subname}"
        return n

    @classmethod
    def error_container(cls, message: str) -> html.Div:
        """Generate the page layout when the page load fails.

        Args:
            message: error message to be rendered.

        Returns:
            `dash.html.Div` container.

        """
        return html.Div(html.Pre(message))

    @classmethod
    @abc.abstractmethod
    def valid_layout(cls, **kwargs):
        """Generate the desired page layout.

        Args:
            kwargs: additional keyword arguments.

        Raises:
            `NotImplementedError`: must be implemented by the subclass.

        """
        raise NotImplementedError

    @classmethod
    def layout(cls, *args, **kwargs):
        """Generate the page layout.

        Args:
            *args: additional positional arguments.
            **kwargs: additional keyword arguments.

        Returns:
            `dash.html.Div` container.

        """
        try:
            return cls.valid_layout(*args, **kwargs)
        except Exception:
            return cls.error_container(traceback.format_exc())
