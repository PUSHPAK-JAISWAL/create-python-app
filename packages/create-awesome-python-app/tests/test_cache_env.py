from typer.testing import CliRunner
from create_awesome_python_app.cli import app
runner = CliRunner()
def test_cache_dir() -> None:
    assert runner.invoke(app, ["cache", "dir"]).exit_code == 0
