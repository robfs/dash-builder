# dash-builder

> [!IMPORTANT]
> `dash-builder` and its developer(s) are not associated with the original `dash` project or its commercial parent, Plotly.

A tool and framework to simplify construction of Python Dash applications.

## API Design

* Create a project in the current working directory
```bash
> dash build
```

* Create project called `testproject` in specified directory
```bash
> dash build testproject --location ~/projects
```

* Add new page to current dash project in pages/ directory
```bash
> dash page NewPage
```

* Add new page to current dash project in specific directory within pages/
```bash
> dash page NewPage --location archive
```

## Installation

`pip install dash-builder`

## Usage

`dash-builder` provides a simple command-line interface (CLI) for initiating and managing your `dash` project.

### Initiating a Dash Project

The `create` command creates a new skeleton project.
It takes a single argument, the name for the new project.
You can use the `--location` option to choose the directory in which to create it.
If no `location` is passed, it will be created in the current working directory.

```bash
❯ dashb create test-project
3/3 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Complete
test-project successfully created in /Users/<username>.
📂 test-project
├── 📂 pages
│   ├── home.py
│   └── not_found_404.py
└── app.py
```

`dash-builder` implements defines 2x classes to be used when building apps:

* `DashPage` - all page modules should define a page object that inherits from this abstract base class.
* `DashView` - all page components should be constructed as views that inerhit from this abstract base class.

## Framework
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

if __name__ == "__main__":
    app.run(debug=True)
```

```python
# pages/home.py
import dash

from dash import html, Input, Output
from dash_builder import DashPage

from views import DemoView, DemoView2, DemoInput, DemoOutput


dash.register_page(__name__, path="/")

class HomePage(DashPage):
    @classmethod
    def valid_layout(cls, **kwargs):
        one = DemoView.create("one")
        two = DemoView.create("two")
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
