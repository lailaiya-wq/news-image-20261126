#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261126 (Python 3.13, stdlib only).

The front page is pre-rendered and committed next to this file as
``entry.png``. This program copies it byte for byte to
``$MAKEFUN_OUTPUT_DIR/entry.png`` (or ``/output/entry.png`` when the
variable is not set), so every run writes the same bytes.
"""

import os
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def main() -> int:
    source = Path(__file__).resolve().parent / IMAGE_NAME
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME
    target.write_bytes(source.read_bytes())
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
