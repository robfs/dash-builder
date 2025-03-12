"""Module containing the AnalyticsPage."""

import dash
import dash_mantine_components as dmc
from dash import html

from dash_builder import DashPage

dash.register_page(__name__)


class AnalyticsPage(DashPage):
    """AnalyticsPage."""

    @classmethod
    def valid_layout(cls, **kwargs):
        """Render valid layout for the AnalyticsPage."""
        return [html.Div(dmc.Title("This is the AnalyticsPage", order=2))]


def layout(**kwargs):
    """Render valid layout for the AnalyticsPage."""
    return AnalyticsPage.layout(**kwargs)
