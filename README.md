# dash-builder

A tool to simplify construction of Python Dash applications.

## Installation

`pip install dash-builder`

## Usage

`dash-builder` leverages existing funcionality from the Dash ecosystem to define a high-level framework that simplifies the construction of complex dashboards.

Under this framework:

* Applications are composed of pages using Dash's multi-page settings.
* Page modules define a page-object that subclasses the `DashPage`.
* Page layouts are collections of views, created by subclassing the `DashView`.
* Views define individual or collections of dash components, or other views.
* Views can be reused to create similar components.
* IDs are managed via the Views to simplify callback management.
* When re-using Views, pattern-matching callbacks can be useful to reduce the number of callbacks.

For example, the below:
* my-dash-project/
  * pages/
    * home.py
  * views/
    * \_\_init\_\_.py
    * demo_input.py
    * demo_output.py
    * demo_view.py
    * demo_view_2.py
  * app.py


```python
# app.py
import dash

from dash import html


app = dash.Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        html.H1("Demo Application"),
        html.Div(dash.page_container)
    ]
)

if __name__ == "__main__:
    app.run(debug=True)
```

```python
# pages/home.py
import dash

from dash import html, Input, Output
from dash_builder import DashPage

from views import DemoView, DemoView2, DemoInput, DemoOutput


class HomePage(DashPage):
    @classmethod
    def valid_layout(cls, **kwargs):
        one = DemoView.create("one")
        two = DemoView,create("two")
        three = DemoView2.create("three")
        return html.Div([one, two, three])

def layout(**kwargs):
    return HomePage.layout(**kwargs)

@dash.callback(
    Output(DemoOutput.matched_id(), "children"),
    Input(DemoInput.matched_id(), "value")
)
def update_value(value: str) -> str:
    return value

@dash.callback(
    Output(DemoView2.id("three", "output"), "children"),
    Input(DemoView2.id("three", "input"), "value")
)
def update_value_2(value: str) -> str:
    return value
```

```python
# views/demo_input.py
from dash import dcc
from dash_builder import DashView


class DemoInput(DashView):
    @classmethod
    def create(cls, id:str, **kwargs) -> dcc.Inupt:
        return dcc.Input(id=cls.id(id))
```

```python
# views/demo_output.py
from dash import html
from dash_builder import DashView


class DemoOutput(DashView):
    @classmethod
    def create(cls, id: str, **kwargs) -> html.Pre:
        return html.Pre(id=cls.id(id))
```

```python
# views/demo_view.py
from dash import html
from dash_builder import DashView

from . import DemoInput, DemoOutput


class DemoView(DashView):
    @classmethod
    def create(cls, id: str, **kwargs) -> html.Span:
        input = DemoInput.create(id)
        output = DemoOutput.create(id)
        return html.Span([input, output], id=cls.id(id))
```

```python
# views/demo_view_2.py
from dash import html, dcc
from dash_builder import DashView


class DemoView2(DashView):
    @classmethod
    def create(cls, id: str, **kwargs) -> html.Span:
        input = dcc.Input(id=cls.id(id, "input"))
        output = html.Pre(id=cls.id(id, "output"))
        return html.Span([input, output], id=cls.id(id))
```
