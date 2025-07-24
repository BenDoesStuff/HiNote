import importlib
import os
import sys
import pytest


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


def test_fail_without_token(monkeypatch):
    monkeypatch.delenv("HINOTE_TOKEN", raising=False)
    sys.modules.pop("hinote.main", None)
    with pytest.raises(RuntimeError):
        importlib.import_module("hinote.main")
