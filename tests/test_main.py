from src.dash_builder.main import app


def test_app(runner):
    result = runner.invoke(app, ["shoot"])
    assert result.exit_code == 0
    assert "Shooting portal gun" in result.stdout
