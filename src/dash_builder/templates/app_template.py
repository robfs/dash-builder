"""Module containing the template for app.py."""

from ._base_template import BaseTemplate

__all__ = ["AppTemplate"]


class AppTemplate(BaseTemplate):
    @classmethod
    def imports(cls) -> str:
        return "import dash\n"

    @classmethod
    def body(cls) -> str:
        return "app: dash.Dash = dash.Dash(__name__, use_pages=True)"

    @classmethod
    def main(cls) -> str:
        return 'if __name__ == "__main__":\n\tapp.run(debug=True)\n'

    @classmethod
    def content_list(cls) -> list[str]:
        return [cls.imports(), cls.body(), cls.main()]
