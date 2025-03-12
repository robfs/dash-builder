"""Module containing the template for a new view."""

from .object_template import ObjectTemplate

__all__ = ["ViewTemplate"]


class ViewTemplate(ObjectTemplate):
    """Template for a new view."""

    _type = "View"

    @property
    def class_comment(self) -> str:
        """Get the class comment of the view."""
        return f'"""{self.class_name}."""'

    @property
    def imports(self) -> str:
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
                f'\t\t"""Render valid layout for the {self.class_name}."""',
                "\t\tweb_id = cls.id(id)",
                f'\t\treturn dmc.Text("This is the {self.class_name}.", id=web_id)\n',
            ]
        )

    @property
    def file_content(self) -> str:
        """Get the file content of the view."""
        return "\n".join([self.module_comment, self.imports, self.class_definition])
