"""Module containing the app sidebar."""

import dash_mantine_components as dmc

from dash_builder import DashView


class SidebarView(DashView):
    """App sidebar."""

    @classmethod
    def valid_layout(cls, id: str, **kwargs):
        """Render valid layout for the SidebarView."""
        return dmc.AppShellNavbar(
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            id=cls.id(id),
            p="md",
            **kwargs,
        )
