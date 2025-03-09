import dash
import dash_mantine_components as dmc
from dash import html
from typing_extensions import override
from views import Footer, Header, Sidebar

from dash_builder import DashPage

dash._dash_renderer._set_react_version("18.2.0")

app: dash.Dash = dash.Dash(
    __name__, use_pages=True, external_stylesheets=dmc.styles.ALL
)


class App(DashPage):
    @override
    @classmethod
    def valid_layout(cls, **kwargs):
        return dmc.AppShell(
            [
                Header.layout("header"),
                Sidebar.layout("sidebar"),
                dmc.AppShellMain(dash.page_container),
                Footer.layout("footer"),
            ],
            header={"height": 60},
            footer={"height": 30},
            navbar={"width": 300},
            padding="md",
            id="app-shell",
        )


app.layout = dmc.MantineProvider(App.layout())


if __name__ == "__main__":
    app.run(debug=True)
