"""Module containing the app header."""

import dash
import dash_mantine_components as dmc

from dash_builder import DashView


class HeaderView(DashView):
    """App header."""

    @classmethod
    def logo(cls, id: str):
        """Logo."""
        return dmc.Group(
            [
                dmc.Image(
                    src="https://thumbs.dreamstime.com/b/logo-du-phoenix-d-oiseau-de-feu-à-gradient-simple-158339374.jpg",
                    h=30,
                ),
                dmc.Title("App Title"),
            ],
            id=cls.id(id, "title"),
        )

    @classmethod
    def nav_links(cls, id: str):
        """Nav links."""
        return dmc.Group(
            [
                dmc.NavLink(label=page["name"], href=page["path"])
                for page in dash.page_registry.values()
                if page["name"] not in {"Not found 404"}
            ],
            wrap="nowrap",
            h="100%",
            p="sm",
            id=cls.id(id, "nav-links"),
        )

    @classmethod
    def valid_layout(cls, id: str, **kwargs):
        """Render valid layout for the HeaderView."""
        return dmc.AppShellHeader(
            dmc.Group(
                [cls.logo(id), cls.nav_links(id)], justify="space-between", px="md"
            ),
            id=cls.id(id),
            **kwargs,
        )
