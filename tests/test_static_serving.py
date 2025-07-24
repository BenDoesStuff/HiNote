import os
import sys
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

import pytest


@pytest.fixture
def uvicorn_server(tmp_path):
    """Start uvicorn server from a different working directory."""
    root = Path(__file__).resolve().parents[1]
    port = 8001
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    cmd = [sys.executable, "-m", "uvicorn", "hinote.main:app", "--port", str(port), "--log-level", "warning"]
    proc = subprocess.Popen(cmd, cwd=str(root.parent), env=env)
    # Wait for server to start
    for _ in range(20):
        try:
            urlopen(f"http://127.0.0.1:{port}/docs")
            break
        except Exception:
            time.sleep(0.5)
    else:
        proc.terminate()
        proc.wait()
        pytest.fail("Server did not start")
    yield port
    proc.terminate()
    proc.wait()


def test_static_files_served(uvicorn_server):
    port = uvicorn_server
    resp = urlopen(f"http://127.0.0.1:{port}/static/styles.css")
    content = resp.read()
    assert b"body" in content
