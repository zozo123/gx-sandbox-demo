"""Pan-provider sandbox runners for the GX Core demo.

Every provider implements the same contract::

    run(script: str = "gx_demo.py") -> str   # executes the script, returns stdout

so the demo runs unchanged across providers. Providers that need an SDK import it
lazily, so this module imports cleanly even without the optional dependency installed.

Status (tracking issue #5):
    islo        implemented, verified         (reference example)
    crabbox     implemented, verified         (Apple container, brokerless)
    daytona     implemented, needs e2e check  (#8)
    modal       planned                       (#6)
    e2b         planned                       (#7)
    tensorlake  N/A - data source, not a sandbox (#9)
"""

from __future__ import annotations

import base64
import subprocess
from pathlib import Path

ISSUES = "https://github.com/zozo123/gx-sandbox-demo/issues"


def _shell(cmd: list[str]) -> str:
    """Run a command, stream its stdout, and return it."""
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(proc.stdout, end="")
    return proc.stdout


def run_islo(script: str = "gx_demo.py", image: str = "python:3.12-slim") -> str:
    """islo.dev cloud microVM. islo does not sync the cwd, so inject over stdin."""
    b64 = base64.b64encode(Path(script).read_bytes()).decode()
    inner = f"pip install -q great_expectations && echo {b64} | base64 -d | python3 -"
    return _shell(["islo", "use", "gx-demo", "-i", image, "--", "bash", "-lc", inner])


def run_crabbox(script: str = "gx_demo.py", image: str = "python:3.12-slim") -> str:
    """crabbox apple-container (local, brokerless). Syncs the git checkout."""
    inner = f"pip install -q great_expectations && python3 {script}"
    return _shell([
        "crabbox", "run", "--provider", "apple-container",
        "--apple-container-image", image, "--", "bash", "-lc", inner,
    ])


def run_daytona(script: str = "gx_demo.py") -> str:
    """Daytona cloud AI sandbox via the Python SDK. Needs DAYTONA_API_KEY."""
    from daytona import Daytona  # lazy: pip install daytona

    daytona = Daytona()
    sandbox = daytona.create()
    try:
        sandbox.process.exec("pip install great_expectations", timeout=600)
        sandbox.fs.upload_file(Path(script).read_bytes(), script)
        out = sandbox.process.exec(f"python {script}", timeout=300).result
        print(out, end="")
        return out
    finally:
        sandbox.delete()


def run_modal(script: str = "gx_demo.py") -> str:
    """Modal serverless containers. See issue #6."""
    raise NotImplementedError(f"Modal runner not implemented yet - see {ISSUES}/6")


def run_e2b(script: str = "gx_demo.py") -> str:
    """E2B Code Interpreter sandboxes. See issue #7."""
    raise NotImplementedError(f"E2B runner not implemented yet - see {ISSUES}/7")


def run_tensorlake(script: str = "gx_demo.py") -> str:
    """Tensorlake is document-ingestion infra, not a code sandbox. See issue #9."""
    raise NotImplementedError(
        "Tensorlake is a document-ingestion / data platform, not a code-execution "
        f"sandbox; it integrates as a data source, not a runner - see {ISSUES}/9"
    )


PROVIDERS: dict[str, dict] = {
    "islo": {"run": run_islo, "status": "verified (reference)"},
    "crabbox": {"run": run_crabbox, "status": "verified"},
    "daytona": {"run": run_daytona, "status": "implemented; verify e2e (#8)"},
    "modal": {"run": run_modal, "status": "planned (#6)"},
    "e2b": {"run": run_e2b, "status": "planned (#7)"},
    "tensorlake": {"run": run_tensorlake, "status": "n/a - data source (#9)"},
}
