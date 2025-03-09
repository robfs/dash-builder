import dash
import dash_mantine_components as dmc
from dash import html
from typing_extensions import override

from dash_builder import DashPage

dash.register_page(__name__, "/")


class Homepage(DashPage):
    @override
    @classmethod
    def valid_layout(cls, **kwargs):
        return [html.H2("This is the page layout")]


def layout(**kwargs):
    return Homepage().layout(**kwargs)
