"""Module containing the abstract DashPage class for defining application pages."""

from ._dash_object import DashObject

__all__ = ["DashPage"]


class DashPage(DashObject):
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
