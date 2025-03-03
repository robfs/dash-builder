import os
import pathlib
import time
import typing
from pathlib import Path

import typer
from rich.console import Console
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.tree import Tree

from .templates import AppTemplate, HomepageTemplate, NotFound404Template

if typing.TYPE_CHECKING:
    from .templates._base_template import BaseTemplate

app = typer.Typer()


class ProjectInitiator:
    def __init__(self, name: str, location: str, **kwargs):
        self.console = Console()
        self.name = name
        self.location = location

        self.path = Path(location)
        self.project = self.path / name

        self.app = self.project / "app.py"

        self.pages = self.project / "pages"
        self.home = self.pages / "home.py"
        self.not_found_404 = self.pages / "not_found_404.py"

    def spinner(self, **kwargs):
        fmt: str = "[progress.description]{task.description}"
        return Progress(SpinnerColumn(), TextColumn(fmt), **kwargs)

    def print_initiation(self):
        absolute_path = self.path.absolute()
        self.console.print(
            f"Initiating [bold green]{self.name}[/bold green] in [bold purple]{absolute_path}[/bold purple]"
        )

    def print_completion(self):
        self.console.print(
            f"[bold green]{self.project}[/bold green] successfully created."
        )

    def check_if_app_exists(self) -> bool:
        if self.app.exists():
            warning = "[bold red]FAILED[/bold red]"
            warning += (
                f"[bold purple]{self.app.absolute()}[/bold purple] already exists."
            )
            warning += "\nPlease remove or rename this file and try again."
            self.console.print(warning)
            return True
        return False

    def create_file(self, path: Path, template: "type[BaseTemplate]"):
        if not path.exists():
            with open(path, "w") as f:
                f.write(template.content())

    def create_directory(self, path: Path):
        if not path.exists():
            os.mkdir(path)

    def TEMP_REMOVE_PROJECT(self):
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
        tree = Tree(
            f":open_file_folder: [link file://{path}][bold green]{path}[/bold green]"
        )
        self.walk_directory(path, tree)
        self.console.print(tree)

    def run(self):
        self.TEMP_REMOVE_PROJECT()
        self.print_initiation()
        already_exists = self.check_if_app_exists()
        if already_exists:
            return None
        with self.spinner(transient=True, console=self.console) as progress:
            progress.add_task("Creating project directory...")
            self.create_directory(self.project)
            progress.add_task("Creating app.py file...")
            self.create_file(self.app, AppTemplate)
            progress.add_task("Creating pages...")
            self.create_directory(self.pages)
            self.create_file(self.home, HomepageTemplate)
            self.create_file(self.not_found_404, NotFound404Template)
        self.print_completion()
        self.print_tree(self.project)


@app.command("init-project")
def init_project(project_name: str, location: str = "."):
    initiator = ProjectInitiator(project_name, location)
    initiator.run()


@app.command("add-page")
def add_page(page_name: str):
    typer.echo(page_name)
