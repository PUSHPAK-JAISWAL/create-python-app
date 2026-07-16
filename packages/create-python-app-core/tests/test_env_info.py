import pytest
from create_python_app_core.api import print_env_info


def test_print_env_info_exits(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as ei:
        print_env_info()
    assert ei.value.code == 0
    out = capsys.readouterr().out
    assert "Python:" in out
    assert "Platform:" in out
