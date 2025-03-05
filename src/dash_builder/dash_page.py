"""Module containing the abstract DashPage class for defining application pages."""

import abc
import traceback

from dash import html

__all__ = ["DashPage"]


class DashPage(abc.ABC):
    """Abstract class for defining pages in a Dash application.

    # Example
    ```python
    import dash
    from dash import html
    from dash_builder import DashPage


    dash.register_page(__name__, path="/")

    class Homepage(Dash):
        @classmethod
        def valid_layout(cls, **kwargs):
            return html.H1("This is the Homepage")

    def layout(**kwargs):
        return Homepage.layout(**kwargs)
    ```
    """

    @classmethod
    def error_container(cls, message):
        return html.Div(html.Pre(message))

    @classmethod
    @abc.abstractmethod
    def valid_layout(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def layout(cls, **kwargs):
        try:
            return cls.valid_layout(**kwargs)
        except Exception:
            return cls.error_container(traceback.format_exc())
