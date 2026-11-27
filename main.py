"""Entry program for the news-image-20261127 make.fun bounty.

The front page itself is drawn by make_front_page.py and stored beside
this file as entry.png. This program's whole job is to place those exact
bytes at /output/entry.png, so every run writes the identical image.
An optional first argument overrides the destination, which is handy
for a local dry run.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
DEFAULT_TARGET = Path("/output/entry.png")


def main(argv):
    if not SOURCE.exists():
        raise SystemExit(f"missing {SOURCE}: run make_front_page.py first")
    target = Path(argv[1]) if len(argv) > 1 else DEFAULT_TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main(sys.argv)
