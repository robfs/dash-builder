import os
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .templates import AppTemplate

app = typer.Typer()


def spinner(**kwargs):
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        **kwargs,
    )


@app.command("init-project")
def init_project(project_name: str, location: str = "."):
    console = Console()
    path = Path(location)
    absolute_path = path.absolute()
    project_path = path / project_name
    app_path = project_path / "app.py"
    if app_path.exists():
        warning = "[bold red]FAILED[/bold red]"
        warning += f"[bold purple]{app_path.absolute()}[/bold purple] already exists."
        warning += "\nPlease remove or rename this file and try again."
        console.print(warning)
        # return
    with spinner(transient=True, console=console) as progress:
        progress.console.print(
            f"Initiating [bold green]{project_name}[/bold green] in [bold purple]{absolute_path}[/bold purple]"
        )

        # create project directory
        task = progress.add_task("Creating project directory...", total=None)
        if not project_path.exists():
            os.mkdir(project_path)

        # generate app file
        progress.update(task, description="Creating app.py file...")
        with open(app_path, "w") as f:
            f.write(AppTemplate.content())

        # generate pages dir
        progress.update(task, description="Creating pages...")
        pages_path = project_path / "pages"
        if not pages_path.exists():
            os.mkdir(pages_path)

        # generate views dir
        progress.update(task, description="Creating views...")
        views_path = project_path / "views"
        views_init_path = views_path / "__init__.py"

        if not views_path.exists():
            os.mkdir(views_path)
        time.sleep(1)
        progress.console.print(
            f"[bold green]{project_name}[/bold green] successfully created."
        )


@app.command("add-page")
def add_page(page_name: str):
    typer.echo(page_name)
