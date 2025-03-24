# tests/test_sentinel_response_config.py
"""Tests para sentinelresponse.config.sentinel_response_config.SentinelResponseConfig."""

import threading
from pathlib import Path

import pytest
import toml

from sentinelresponse.config.sentinel_response_config import SentinelResponseConfig

BASE_CONFIG = {
    "main": {"foo": "bar"},
    "notification": {"email": "user@example.com"},
    "log": {"level": "DEBUG"},
}

UPDATED_CONFIG = {
    "main": {"foo": "baz"},
    "notification": {"email": "another@example.com"},
    "log": {"level": "INFO"},
}


@pytest.fixture(autouse=True)
def reset_singleton():
    SentinelResponseConfig._instance = None
    yield
    SentinelResponseConfig._instance = None


def write_toml(tmp_path: Path, content: dict) -> Path:
    path = tmp_path / "config.toml"
    path.write_text(toml.dumps(content))
    return path


def test_singleton_behavior(tmp_path):
    path = write_toml(tmp_path, BASE_CONFIG)
    cfg1 = SentinelResponseConfig(toml_path=str(path))
    cfg2 = SentinelResponseConfig(toml_path=str(path))
    assert cfg1 is cfg2  # nosec


def test_loads_sections_correctly(tmp_path):
    path = write_toml(tmp_path, BASE_CONFIG)
    cfg = SentinelResponseConfig(toml_path=str(path))
    assert cfg.main == BASE_CONFIG["main"]  # nosec
    assert cfg.notification == BASE_CONFIG["notification"]  # nosec
    assert cfg.log == BASE_CONFIG["log"]  # nosec


def test_repr_contains_sections(tmp_path):
    path = write_toml(tmp_path, BASE_CONFIG)
    cfg = SentinelResponseConfig(toml_path=str(path))
    rep = repr(cfg)
    assert "<SentinelResponseConfig(" in rep  # nosec
    for section in ("main", "notification", "log"):
        assert f"{section}=" in rep  # nosec


def test_reload_updates_values(tmp_path):
    path = write_toml(tmp_path, BASE_CONFIG)
    cfg = SentinelResponseConfig(toml_path=str(path))
    new_path = write_toml(tmp_path, UPDATED_CONFIG)
    cfg.reload(toml_path=str(new_path))
    assert cfg.main == UPDATED_CONFIG["main"]  # nosec
    assert cfg.notification == UPDATED_CONFIG["notification"]  # nosec
    assert cfg.log == UPDATED_CONFIG["log"]  # nosec


def test_reload_defaults_to_previous_path(tmp_path):
    path = write_toml(tmp_path, BASE_CONFIG)
    cfg = SentinelResponseConfig(toml_path=str(path))
    path.write_text(toml.dumps(UPDATED_CONFIG))
    cfg.reload()
    assert cfg.main == UPDATED_CONFIG["main"]  # nosec


def test_file_not_found_on_init(tmp_path):
    missing = tmp_path / "does_not_exist.toml"
    with pytest.raises(FileNotFoundError):
        SentinelResponseConfig(toml_path=str(missing))


def test_file_not_found_on_reload(tmp_path):
    path = write_toml(tmp_path, BASE_CONFIG)
    cfg = SentinelResponseConfig(toml_path=str(path))
    with pytest.raises(FileNotFoundError):
        cfg.reload(toml_path=str(tmp_path / "missing.toml"))


def test_thread_safety(tmp_path):
    path = write_toml(tmp_path, BASE_CONFIG)
    instances = []

    def create_instance():
        instances.append(SentinelResponseConfig(toml_path=str(path)))

    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert all(inst is instances[0] for inst in instances)  # nosec
