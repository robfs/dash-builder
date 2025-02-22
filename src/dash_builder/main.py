import os
import time
import typing
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .templates import AppTemplate, HomepageTemplate

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

    def check_if_app_exists(self):
        if self.app.exists():
            warning = "[bold red]FAILED[/bold red]"
            warning += (
                f"[bold purple]{self.app.absolute()}[/bold purple] already exists."
            )
            warning += "\nPlease remove or rename this file and try again."
            self.console.print(warning)

    def create_file(self, path: Path, template: "type[BaseTemplate]"):
        if not path.exists():
            with open(path, "w") as f:
                f.write(template.content())

    def create_directory(self, path: Path):
        if not path.exists():
            os.mkdir(path)

    def run(self):
        self.print_initiation()
        self.check_if_app_exists()
        with self.spinner(transient=True, console=self.console) as progress:
            progress.add_task("Creating project directory...")
            self.create_directory(self.project)
            progress.add_task("Creating app.py file...")
            self.create_file(self.app, AppTemplate)
            progress.add_task("Creating pages...")
            self.create_directory(self.pages)
            self.create_file(self.home, HomepageTemplate)
        self.print_completion()


@app.command("init-project")
def init_project(project_name: str, location: str = "."):
    initiator = ProjectInitiator(project_name, location)
    initiator.run()


@app.command("add-page")
def add_page(page_name: str):
    typer.echo(page_name)
