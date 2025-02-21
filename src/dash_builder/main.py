import time
from pathlib import Path

import typer

from rich.progress import Progress, TextColumn, SpinnerColumn

app = typer.Typer()


def spinner(**kwargs):
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        **kwargs,
    )


@app.command("init-project")
def init_project(project_name: str, location: str = "."):
    path = Path(location)
    absolute_path = path.absolute()
    with spinner(transient=True) as progress:
        progress.console.print(
            f"Initiating [bold green]{project_name}[/bold green] in [bold purple]{absolute_path}[/bold purple]"
        )
        # create project directory
        task = progress.add_task(f"Creating project directory...", total=None)
        time.sleep(1)
        # generate app file
        progress.update(task, description="Creating app.py file...")
        time.sleep(1)
        # generate pages dir
        progress.update(task, description="Creating pages...")
        time.sleep(1)
        # generate views dir
        progress.update(task, description="Creating views...")
        time.sleep(1)
        progress.console.print(
            f"[bold green]{project_name}[/bold green] successfully created."
        )


@app.command("add-page")
def add_page(page_name: str):
    typer.echo(page_name)
