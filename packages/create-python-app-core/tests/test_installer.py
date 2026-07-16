from pathlib import Path

import pytest
from create_python_app_core.installer import scaffold_project


def _tpl(tmp: Path, name: str) -> str:
    root = tmp / name
    (root / "template").mkdir(parents=True)
    (root / "template" / "hello.txt").write_text("hi")
    (root / "cpa.config.json").write_text('{"name":"t"}')
    return f"file://{root}"


def test_scaffold_file_template(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CPA_SKIP_GIT", "1")
    dest = tmp_path / "app"
    url = _tpl(tmp_path, "tpl")
    scaffold_project(str(dest), template=url, install=False)
    assert (dest / "hello.txt").read_text() == "hi"
