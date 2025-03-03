from src.dash_builder.main import app


def test_init_project_cli(runner, tmp_path):
    result = runner.invoke(app, ["init-project", str(tmp_path)])
    app_file = tmp_path / "app.py"
    pages = tmp_path / "pages"
    homepage = pages / "home.py"
    not_found_404 = pages / "not_found_404.py"
    assert result.exit_code == 0
    # TODO: remove deletion
    assert f"DELETING {tmp_path}" in result.stdout.replace("\n", "")
    assert f"{tmp_path} successfully created." in result.stdout.replace("\n", "")
    assert tmp_path.exists()
    assert app_file.exists()
    assert pages.exists()
    assert homepage.exists()
    assert not_found_404.exists()
