"""Module containing the main `typer` CLI for managing dash projects."""

import os
import pathlib
import typing
from pathlib import Path

import typer
from rich.console import Console
from rich.markup import escape
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn
from rich.text import Text
from rich.tree import Tree

from .templates import AppTemplate, HomepageTemplate, NotFound404Template

if typing.TYPE_CHECKING:
    from .templates._base_template import BaseTemplate

app: typer.Typer = typer.Typer()
"""The `typer.Typer` applicaiton object."""


class ProjectInitiator:
    """Object to capture and process project initiation options and logic."""

    def __init__(self, name: str, location: str, **kwargs):
        """Create project initiation class.

        Args:
            name: the name of the project (used for the project directory).
            location: the destination directory for the project.
            **kwargs: additional keyword arguments.

        """
        self.console: Console = Console()
        """`rich.Console` object for printing to stdout."""
        self.name: str = name
        """Project name."""
        self._location: str = location
        """Project destination directory."""

        self.templates: "list[type[BaseTemplate]]" = [
            AppTemplate,
            HomepageTemplate,
            NotFound404Template,
        ]
        """List of template files to create as part of the project."""

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
        return Progress(MofNCompleteColumn(), BarColumn(), TextColumn(fmt), **kwargs)

    def print_completion(self):
        """Print confirmation of project initiation."""
        self.console.print(
            f"[bold green]{self.project}[/bold green] successfully created in [bold purple]{self.location.absolute()}[/bold purple]."
        )

    def check_if_app_exists(self) -> bool:
        """Check if the `app.py` file already exists."""
        app_path = self.project / AppTemplate.path
        if app_path.exists():
            warning = "[bold red]FAILED[/bold red]"
            warning += (
                f"[bold purple]{app_path.absolute()}[/bold purple] already exists."
            )
            warning += "\nPlease remove or rename this file and try again."
            self.console.print(warning)
            return True
        return False

    def create_file_from_template(self, template: "type[BaseTemplate]"):
        """Create a projet file from a template."""
        file_path = self.project / template.path
        parent = file_path.parent
        if not parent.exists():
            parent.mkdir(exist_ok=True, parents=True)
        if not file_path.exists():
            file_path.write_text(template.content())

    def _TEMP_REMOVE_PROJECT(self):
        if self.project.exists():
            import shutil

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

    def run(self):
        """Run the project initiation."""
        # self._TEMP_REMOVE_PROJECT()
        already_exists = self.check_if_app_exists()
        if already_exists:
            return None
        with self.spinner(console=self.console) as progress:
            task = progress.add_task("Creating project", total=len(self.templates))
            for template in self.templates:
                progress.update(task, description=f"Creating {template.path}")
                self.create_file_from_template(template)
                progress.update(task, advance=1)
            progress.update(task, description="Complete")
        os.system(f"ruff format {self.project}")
        os.system(f"ruff check --select I --fix {self.project}")
        self.print_completion()
        self.print_tree(self.project)


@app.command("create")
def create(project_name: str, location: str = "."):
    """Initialise a new Dash Builder project.

    Args:
        project_name: the name of the project (used for the project directory).
        location: the destination directory for the project.

    """
    initiator = ProjectInitiator(project_name, location)
    initiator.run()


@app.command("add-page")
def add_page(page_name: str):
    """Add a new page to the project.

    Args:
        page_name: the name of the page to add.

    """
    typer.echo(page_name)
