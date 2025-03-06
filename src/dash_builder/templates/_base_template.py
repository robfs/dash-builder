"""Module containing the base template for generating project files."""

import abc
from pathlib import Path

__all__ = ["BaseTemplate"]


class BaseTemplate(abc.ABC):
    """Abstract template class for building project files."""

    path: Path = Path(".")
    """Path to the file to be generated."""
    _dash_imports: list[str] = []
    """List of imports from the `dash` package."""
    _dash_builder_imports: list[str] = []
    """List of imports from the `dash_builder` package."""

    @classmethod
    def create_import_string(cls, package: str, import_list: list[str]) -> str:
        """Create an import string for the given package and import list.

        Args:
            package: name of the package to import from.
            import_list: list of imports to include.

        """
        imports = ""
        if import_list:
            imports += f"from {package} import "
            imports += ", ".join(import_list)
        return imports

    @classmethod
    def get_dash_imports(cls) -> str:
        """Get the import string for the `dash` package.

        Returns:
            import string for the `dash` package.

        """
        imports = "import dash\n"
        imports += cls.create_import_string("dash", cls._dash_imports)
        return imports

    @classmethod
    def get_dash_builder_imports(cls) -> str:
        """Get the import string for the `dash_builder` package.

        Returns:
            import string for the `dash_builder` package.

        """
        return cls.create_import_string("dash_builder", cls._dash_builder_imports)

    @classmethod
    def page_imports(cls) -> str:
        """Get the import string for the page.

        Returns:
            import string for the page.

        """
        imports: list[str] = [cls.get_dash_imports(), cls.get_dash_builder_imports()]
        return "\n".join(imports)

    @staticmethod
    def register_page(path: str | None) -> str:
        """Create a `dash.register_page` call.

        Args:
            path: URL path to the page.

        Returns:
            `dash.register_page` call.

        """
        args = "__name__"
        if path is not None:
            args += f', "{path}"'
        return f"dash.register_page({args})"

    @classmethod
    def get_page_name(cls) -> str:
        """Get the name of the page.

        Returns:
            name of the page.

        """
        return cls.__name__.replace("Template", "")

    @classmethod
    def get_page_class(cls, layout: str) -> str:
        """Get the string representation of the page class.

        Args:
            layout: string representation of the page layout.

        Returns:
            Page class definition as a string.

        """
        lines = (
            f"class {cls.get_page_name()}(DashPage):",
            "\t@classmethod",
            "\tdef valid_layout(cls, **kwargs):",
            f"\t\treturn {layout}",
        )
        return "\n".join(lines)

    @classmethod
    def get_layout_function(cls) -> str:
        """Get the string representation of the page layout function, required by `dash` pages.

        Returns:
            string representation of the page layout function.

        """
        return f"def layout(**kwargs):\n\treturn {cls.get_page_name()}().layout(**kwargs)"

    @classmethod
    def get_default_page_contents(
        cls, path: str | None = None, layout: str = "[]"
    ) -> tuple[str, str, str, str]:
        """Get the default contents for a dash page.

        Args:
            path: URL path to the page.
            layout: string representation of the page layout.

        Returns:
            tuple of imports, register call, page class, layout function.

        """
        return (
            cls.page_imports(),
            cls.register_page(path),
            cls.get_page_class(layout=layout),
            cls.get_layout_function(),
        )

    @classmethod
    @abc.abstractmethod
    def content_list(cls) -> list[str]:
        """Get list of string representations of the contents of the page.

        Raises:
            NotImplementedError: if the method is not implemented.

        """
        raise NotImplementedError

    @classmethod
    def content(cls) -> str:
        """Get the string representation of the page contents.

        Returns:
            string representation of the page contents.

        """
        return "\n\n\n".join(cls.content_list())
