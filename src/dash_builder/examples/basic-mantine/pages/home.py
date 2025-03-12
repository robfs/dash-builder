"""Module containing the HomePage."""

import dash
import dash_mantine_components as dmc
from dash import html

from dash_builder import DashPage

dash.register_page(__name__, path="/")


class HomePage(DashPage):
    """HomePage."""

    @classmethod
    def valid_layout(cls, **kwargs):
        """Render valid layout for the HomePage."""
        return [html.Div(dmc.Title("This is the HomePage", order=2))]


def layout(**kwargs):
    """Render valid layout for the HomePage."""
    return HomePage.layout(**kwargs)
