"""Tests for the main `typer` CLI."""

import pytest

from src.dash_builder.main import app
from src.dash_builder.templates import (
    AppTemplate,
    HomepageTemplate,
    NotFound404Template,
)


@pytest.mark.parametrize(
    "project_name", ["test-project-1", "test_project_2", "testproject"]
)
def test_init_project_cli(runner, tmp_path, project_name):
    app_params = ["init-project", project_name, "--location", str(tmp_path)]
    result = runner.invoke(app, app_params)
    project = tmp_path / project_name
    app_file = project / AppTemplate.path
    pages = project / "pages"
    homepage = project / HomepageTemplate.path
    not_found_404 = project / NotFound404Template.path
    assert result.exit_code == 0
    assert (
        f"{project_name} successfully created in {tmp_path}"
        in result.stdout.replace("\n", "")
    )
    assert tmp_path.exists()
    assert app_file.exists()
    assert pages.exists()
    assert homepage.exists()
    assert not_found_404.exists()
