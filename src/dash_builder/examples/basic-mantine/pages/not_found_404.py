"""Module containing the NotFound404."""

import dash
import dash_mantine_components as dmc
from dash import html

from dash_builder import DashPage

dash.register_page(__name__)


class NotFound404(DashPage):
    """NotFound404."""

    @classmethod
    def valid_layout(cls, **kwargs):
        """Render valid layout for the NotFound404."""
        return [
            html.Div(
                dmc.Image(
                    src="https://img.freepik.com/free-vector/hand-drawn-404-error_23-2147746234.jpg",
                    style={"margin": "auto", "display": "flex"},
                )
            )
        ]


def layout(**kwargs):
    """Render valid layout for the NotFound404."""
    return NotFound404().layout(**kwargs)
