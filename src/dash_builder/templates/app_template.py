"""Module containing the template for app.py."""

from ._base_template import BaseTemplate

__all__ = ["AppTemplate"]


class AppTemplate(BaseTemplate):
    @staticmethod
    def imports() -> str:
        return "import dash\n"

    @staticmethod
    def body() -> str:
        return "app: dash.Dash = dash.Dash(__name__, use_pages=True)"

    @staticmethod
    def main() -> str:
        return 'if __name__ == "__main__":\n\tapp.run(debug=True)\n'

    @classmethod
    def content_list(cls) -> list[str]:
        return [cls.imports(), cls.body(), cls.main()]
