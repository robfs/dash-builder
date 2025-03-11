"""Module containing the main `typer` CLI for managing dash projects."""

import pathlib
import shutil
from pathlib import Path

import typer
from rich.console import Console
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.tree import Tree
from typing_extensions import Annotated

app: typer.Typer = typer.Typer()
"""The `typer.Typer` applicaiton object."""


class Project:
    """Object to capture and process project initiation options and logic."""

    def __init__(self, name: str, template: str, location: str, **kwargs):
        """Create project initiation class.

        Args:
            name: the name of the project (used for the project directory).
            template: the template to use for the project.
            location: the destination directory for the project.
            **kwargs: additional keyword arguments.

        """
        self.console: Console = Console()
        """`rich.Console` object for printing to stdout."""
        self.name: str = name.replace(" ", "-")
        """Project name."""
        self._template: str = template
        """Project template."""
        self._location: str = location
        """Project destination directory."""

    @property
    def template(self) -> Path:
        """Template directory."""
        return Path(__file__).parent / "examples" / self._template

    @property
    def location(self) -> Path:
        """Destination directory for the project."""
        return Path(self._location)

    @property
    def project(self) -> Path:
        """Project directory."""
        return self.location / self.name

    def spinner(self, **kwargs):
        """Customised `rich.Progress` bar."""
        fmt: str = "[progress.description]{task.description}"
        return Progress(SpinnerColumn(), TextColumn(fmt), **kwargs)

    def print_completion(self):
        """Print confirmation of project initiation."""
        self.console.print(
            f"[bold green]{self.project}[/bold green] successfully created in [bold purple]{self.location.absolute()}[/bold purple]."
        )

    def check_if_app_exists(self) -> bool:
        """Check if the `app.py` file already exists."""
        app_path = self.project / "app.py"
        if app_path.exists():
            warning = "[bold red]FAILED[/bold red]"
            warning += (
                f"[bold purple]{app_path.absolute()}[/bold purple] already exists."
            )
            warning += "\nPlease remove or rename this file and try again."
            self.console.print(warning)
            return True
        return False

    def _TEMP_REMOVE_PROJECT(self):
        if self.project.exists():
            self.console.print(f"[bold red]DELETING {self.project}[/bold red]")
            shutil.rmtree(self.project)

    def walk_directory(self, directory: pathlib.Path, tree: Tree) -> None:
        """Recursively build a Tree with directory contents."""
        # Sort dirs first then by filename
        paths = sorted(
            directory.iterdir(),
            key=lambda path: (path.is_file(), path.name.lower()),
        )
        for path in paths:
            # Remove hidden files
            if path.name.startswith("."):
                continue
            if path.is_dir():
                style = "dim" if path.name.startswith("__") else ""
                branch = tree.add(
                    f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}",
                    style=style,
                    guide_style=style,
                )
                self.walk_directory(path, branch)
            else:
                text_filename = Text(path.name, "blue")
                tree.add(text_filename)

    def print_tree(self, path: Path):
        """Print the directory tree for a path."""
        tree = Tree(
            f":open_file_folder: [link file://{path}][bold green]{path}[/bold green]"
        )
        self.walk_directory(path, tree)
        self.console.print(tree)

    def build(self):
        """Run the project initiation."""
        if not self.template.exists() or not self.template.is_dir():
            self.console.print(
                f"[bold red]Error:[/bold red] Template '{self._template}' not found in examples."
            )
            return None
        self._TEMP_REMOVE_PROJECT()
        already_exists = self.check_if_app_exists()
        if already_exists:
            return None
        with self.spinner(console=self.console, transient=True) as progress:
            progress.add_task("Creating project")
            to_ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
            output = shutil.copytree(self.template, self.project, ignore=to_ignore)
        self.print_completion()
        self.print_tree(output.absolute())


@app.command("build")
def build(
    project_name: Annotated[str, typer.Argument(help="The name of the project.")],
    template: Annotated[
        str, typer.Argument(help="The template to use for the project.")
    ] = "basic-mantine",
    location: Annotated[
        str, typer.Option(help="The destination directory for the project.")
    ] = ".",
):
    """Initialise a new Dash Builder project.

    Args:
        project_name: the name of the project (used for the project directory).
        template: the template to use for the project.
        location: the destination directory for the project.

    """
    initiator = Project(project_name, template, location)
    initiator.build()


@app.command("add-page")
def add_page(page_name: str):
    """Add a new page to the project.

    Args:
        page_name: the name of the page to add.

    """
    typer.echo(page_name)
