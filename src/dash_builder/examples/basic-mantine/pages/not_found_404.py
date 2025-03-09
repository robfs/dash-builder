import dash
import dash_mantine_components as dmc
from dash import html

from dash_builder import DashPage

dash.register_page(__name__)


class NotFound404(DashPage):
    @classmethod
    def valid_layout(cls, **kwargs):
        return [
            html.Img(
                src="https://img.freepik.com/free-vector/hand-drawn-404-error_23-2147746234.jpg",
                style={"margin": "auto", "display": "flex"},
            )
        ]


def layout(**kwargs):
    return NotFound404().layout(**kwargs)
