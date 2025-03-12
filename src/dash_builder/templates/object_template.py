"""Module containing the abstract template for a new object."""

import abc
import re
from pathlib import Path

__all__ = ["ObjectTemplate"]


class ObjectTemplate(abc.ABC):
    """Template for a new object."""

    _type: str = "Object"
    pascal_pattern = re.compile(r"(?<!^)(?=[A-Z])")

    def __init__(self, name: str, path: Path):
        """Initialize the object template."""
        self.name: str = name
        self.path: Path = path
        self.file_path: Path = path / self.file_name

    @classmethod
    def to_snake_case(cls, value: str) -> str:
        """Convert the name from PascalCase to snake_case using regex."""
        return cls.pascal_pattern.sub("_", value).lower()

    @property
    def file_name(self) -> str:
        """Get the file name of the object."""
        return f"{self.to_snake_case(self.name)}.py"

    @property
    def class_name(self) -> str:
        """Get the class name of the object."""
        return self.name[0].upper() + self.name[1:] + self._type

    @property
    def module_comment(self) -> str:
        """Get the module comment of the object."""
        return f'"""Module containing the {self.class_name}."""\n'

    @abc.abstractmethod
    def imports(self) -> list[str]:
        """Get the imports of the object."""
        raise NotImplementedError

    @abc.abstractmethod
    def class_definition(self) -> str:
        """Get the class definition of the object."""
        raise NotImplementedError

    @abc.abstractmethod
    def file_content(self) -> str:
        """Get the file content of the object."""
        raise NotImplementedError
