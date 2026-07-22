from create_awesome_python_app.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def _out(result) -> str:
    return (result.stdout or "") + (result.stderr or "")


def test_list_templates() -> None:
    result = runner.invoke(app, ["--list-templates"])
    assert result.exit_code == 0
    text = _out(result)
    assert "Available Templates" in text


def test_list_addons() -> None:
    result = runner.invoke(app, ["--list-addons"])
    assert result.exit_code == 0
    assert "Available Addons" in _out(result)
