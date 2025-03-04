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

app = typer.Typer()


class ProjectInitiator:
    def __init__(self, name: str, location: str, **kwargs):
        self.console = Console()
        self.name = name
        self.location = location

        self.path = Path(location)
        self.project = self.path / name

        self.templates: "list[type[BaseTemplate]]" = [
            AppTemplate,
            HomepageTemplate,
            NotFound404Template,
        ]

    def spinner(self, **kwargs):
        fmt: str = "[progress.description]{task.description}"
        return Progress(MofNCompleteColumn(), BarColumn(), TextColumn(fmt), **kwargs)

    def print_completion(self):
        self.console.print(
            f"[bold green]{self.project}[/bold green] successfully created in [bold purple]{self.path.absolute()}[/bold purple]."
        )

    def check_if_app_exists(self) -> bool:
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
        file_path = self.project / template.path
        parent = file_path.parent
        if not parent.exists():
            parent.mkdir(exist_ok=True, parents=True)
        if not file_path.exists():
            file_path.write_text(template.content())

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
        self.print_completion()
        self.print_tree(self.project)


@app.command("init-project")
def init_project(project_name: str, location: str = "."):
    initiator = ProjectInitiator(project_name, location)
    initiator.run()


@app.command("add-page")
def add_page(page_name: str):
    typer.echo(page_name)
