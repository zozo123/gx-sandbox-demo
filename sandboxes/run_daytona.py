"""Run the GX demo in a Daytona AI sandbox.

Daytona does not auto-sync local files, so we upload gx_demo.py and then exec it.
This follows Daytona's documented Python SDK (https://www.daytona.io/docs); it is
NOT executed in this repo's CI because it requires an API key.

Prereqs:
    pip install daytona
    export DAYTONA_API_KEY=...   # from app.daytona.io

Usage:
    python sandboxes/run_daytona.py
"""

from pathlib import Path

from daytona import Daytona


def main() -> None:
    daytona = Daytona()  # reads DAYTONA_API_KEY from the environment
    sandbox = daytona.create()
    try:
        sandbox.process.exec("pip install great_expectations", timeout=600)
        sandbox.fs.upload_file(Path("gx_demo.py").read_bytes(), "gx_demo.py")
        result = sandbox.process.exec("python gx_demo.py", timeout=300)
        print(result.result)
    finally:
        sandbox.delete()  # stop compute billing


if __name__ == "__main__":
    main()
