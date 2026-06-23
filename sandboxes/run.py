"""Pan-provider CLI: run the GX demo in a sandbox.

Usage:
    python sandboxes/run.py --list
    python sandboxes/run.py islo [script.py]
    python sandboxes/run.py crabbox

Each provider implements the same run(script) contract in providers.py.
"""

from __future__ import annotations

import argparse
import sys

from providers import PROVIDERS


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the GX demo in a sandbox provider.")
    parser.add_argument("provider", nargs="?", choices=sorted(PROVIDERS), help="provider name")
    parser.add_argument("script", nargs="?", default="gx_demo.py", help="script to run")
    parser.add_argument("--list", action="store_true", help="list providers and exit")
    args = parser.parse_args()

    if args.list or not args.provider:
        width = max(len(name) for name in PROVIDERS)
        for name, meta in sorted(PROVIDERS.items()):
            print(f"{name:<{width}}  {meta['status']}")
        return 0

    PROVIDERS[args.provider]["run"](args.script)
    return 0


if __name__ == "__main__":
    sys.exit(main())
