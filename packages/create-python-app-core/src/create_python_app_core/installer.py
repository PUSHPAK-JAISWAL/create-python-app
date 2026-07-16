"""Scaffold orchestrator: copy layers → optional uv sync → git init."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from create_python_app_core.config import assert_directory_is_empty, load_cpa_config
from create_python_app_core.errors import CpaError, ScaffoldAbortedError
from create_python_app_core.git_cache import download_repository
from create_python_app_core.loaders import merge_layers
from create_python_app_core.paths import ResolvedSource, resolve_source


def _run(cmd: list[str], *, cwd: Path) -> None:
    subprocess.check_call(cmd, cwd=str(cwd))


def init_git_repo(dest: Path) -> None:
    if (dest / ".git").exists():
        return
    _run(["git", "init"], cwd=dest)


def uv_sync(dest: Path) -> None:
    _run(["uv", "sync"], cwd=dest)


def scaffold_project(
    project_directory: str,
    *,
    template: str,
    addons: list[str] | None = None,
    extend: list[str] | None = None,
    force: bool = False,
    install: bool = True,
    offline: bool = False,
    keep_on_failure: bool = False,
    cache_dir: Path | None = None,
    options: dict[str, Any] | None = None,
) -> Path:
    """Create a project directory from template + addon layers."""
    _ = options
    dest = Path(project_directory).expanduser().resolve()
    assert_directory_is_empty(dest, force=force)
    dest.mkdir(parents=True, exist_ok=True)

    specs = [template, *(addons or []), *(extend or [])]
    layers: list[tuple[ResolvedSource, Path]] = []
    try:
        for spec in specs:
            source = resolve_source(spec, cache_dir=cache_dir)
            root = download_repository(source, offline=offline, cache_root=cache_dir)
            layers.append((source, root))
            cfg_path = root / "cpa.config.json"
            if not cfg_path.is_file() and source.subdir:
                cfg_path = root / source.subdir / "cpa.config.json"
            load_cpa_config(cfg_path)

        merge_layers(layers, dest)

        if install and (dest / "pyproject.toml").is_file():
            uv_sync(dest)
        if os.environ.get("CPA_SKIP_GIT") != "1":
            init_git_repo(dest)
    except Exception as exc:
        if not keep_on_failure and dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
        if isinstance(exc, CpaError):
            raise
        raise ScaffoldAbortedError(str(exc)) from exc
    return dest
