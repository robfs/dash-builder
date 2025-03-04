"""Module containing the base template for generating project files."""

import abc

__all__ = ["BaseTemplate"]


class BaseTemplate(abc.ABC):
    _dash_imports: list[str] = []
    _dash_builder_imports: list[str] = []

    @classmethod
    def create_import_string(cls, package: str, import_list: list[str]) -> str:
        imports = ""
        if import_list:
            imports += f"from {package} import "
            imports += ", ".join(import_list)
        return imports

    @classmethod
    @property
    def dash_imports(cls) -> str:
        imports = "import dash\n"
        imports += cls.create_import_string("dash", cls._dash_imports)
        return imports

    @classmethod
    @property
    def dash_builder_imports(cls) -> str:
        return cls.create_import_string("dash_builder", cls._dash_builder_imports)

    @classmethod
    def page_imports(cls) -> str:
        imports: list[str] = [cls.dash_imports, cls.dash_builder_imports]
        return "\n".join(imports)

    @staticmethod
    def register_page(path: str | None) -> str:
        args = "__name__"
        if path is not None:
            args += f', "{path}"'
        return f"dash.register_page({args})"

    @classmethod
    @property
    def page_name(cls) -> str:
        return cls.__name__.replace("Template", "")

    @classmethod
    def page_class(cls, layout: str) -> str:
        lines = (
            f"class {cls.page_name}(DashPage):",
            "\t@classmethod",
            "\tdef valid_layout(cls, **kwargs):",
            f"\t\treturn {layout}",
        )
        return "\n".join(lines)

    @classmethod
    def layout_function(cls) -> str:
        return f"def layout(**kwargs):\n\treturn {cls.page_name}().layout(**kwargs)"

    @classmethod
    def page_default_contents(
        cls, path: str | None = None, layout: str = "[]"
    ) -> tuple[str, str, str, str]:
        return (
            cls.page_imports(),
            cls.register_page(path),
            cls.page_class(layout=layout),
            cls.layout_function(),
        )

    @classmethod
    @abc.abstractmethod
    def content_list(cls) -> list[str]:
        raise NotImplementedError

    @classmethod
    def content(cls) -> str:
        return "\n\n\n".join(cls.content_list())
