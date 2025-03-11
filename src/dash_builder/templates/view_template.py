"""Module containing the template for a new view."""

import re
from pathlib import Path

__all__ = ["ViewTemplate"]


class ViewTemplate:
    """Template for a new view."""

    pascal_pattern = re.compile(r"(?<!^)(?=[A-Z])")

    def __init__(self, name: str, path: Path):
        """Initialize the view template."""
        self.name: str = name
        self.path: Path = path
        self.file_path: Path = path / self.file_name

    @classmethod
    def to_snake_case(cls, value: str) -> str:
        """Convert the name from PascalCase to snake_case using regex."""
        return cls.pascal_pattern.sub("_", value).lower()

    @property
    def file_name(self) -> str:
        """Get the file name of the view."""
        return f"{self.to_snake_case(self.name)}.py"

    @property
    def class_name(self) -> str:
        """Get the class name of the view."""
        return self.name[0].upper() + self.name[1:]

    @property
    def module_comment(self) -> str:
        """Get the module comment of the view."""
        return f'"""Module containing the {self.class_name} view."""\n'

    @property
    def class_comment(self) -> str:
        """Get the class comment of the view."""
        return f'"""{self.class_name} view."""'

    @property
    def imports(self) -> list[str]:
        """Get the imports of the view."""
        return "\n".join(
            [
                "import dash_mantine_components as dmc\n",
                "from dash_builder import DashView\n\n",
            ]
        )

    @property
    def class_definition(self) -> str:
        """Get the class definition of the view."""
        return "\n".join(
            [
                f"class {self.class_name}(DashView):",
                f"\t{self.class_comment}\n",
                "\t@classmethod",
                "\tdef valid_layout(cls, id: str, **kwargs):",
                f'\t\t"""Render valid layout for the {self.class_name} view."""',
                "\t\tweb_id = cls.id(id)",
                f'\t\treturn dmc.Text("This is the {self.class_name} view.", id=web_id)\n',
            ]
        )

    @property
    def file_content(self) -> str:
        """Get the file content of the view."""
        return "\n".join([self.module_comment, self.imports, self.class_definition])
