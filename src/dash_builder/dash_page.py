import abc
import traceback

from dash import html

__all__ = ["DashPage"]


class DashPage(abc.ABC):
    @classmethod
    def error_container(cls, message):
        return html.Div(html.Pre(message))

    @classmethod
    @abc.abstractmethod
    def valid_layout(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def layout(cls, **kwargs):
        try:
            return cls.valid_layout(**kwargs)
        except Exception:
            return cls.error_container(traceback.format_exc())
