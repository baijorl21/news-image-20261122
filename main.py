#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261122.

The entry image is the entry.png beside this file - a newspaper front
page summing up the world news of Sunday 22 November 2026, drawn from
scratch by make_image.py (PIL primitives only, no photos, no network).
This program copies it to /output/entry.png; both grader runs write the
same bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        raise SystemExit(f"entry image missing: {source}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / "entry.png")


if __name__ == "__main__":
    main()
