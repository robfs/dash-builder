"""Module containing the app footer."""

import dash_mantine_components as dmc

from dash_builder import DashView


class FooterView(DashView):
    """App footer."""

    @classmethod
    def valid_layout(cls, id: str, **kwargs):
        """Render valid layout for the FooterView."""
        return dmc.AppShellFooter(
            dmc.Text("Dash-Builder is not affiliated with Plotly or Dash"),
            ta="center",
            id=cls.id(id),
            **kwargs,
        )
