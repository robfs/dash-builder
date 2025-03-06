"""Package to assist in building Dash apps.

# Installation

* Using `pip` - `pip install dash-builder`
* Using `uv` - `uv add dash-builder`
"""

from . import cli, dash_page, dash_view
from .dash_page import DashPage
from .dash_view import DashView

__all__ = ["DashPage", "DashView", "cli", "dash_page", "dash_view"]
