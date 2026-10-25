#!/usr/bin/env python3
"""Write the transparent Xcursor shapes this theme hides.

The images stay out of git. The marketplace scanner cannot read those blobs.
"""

import pathlib

# 1x1 transparent Xcursor, nominal size 24, hotspot at 0,0.
BLOB = bytes.fromhex(
    "586375721000000000000100010000000200fdff18000000"
    "1c000000240000000200fdff180000000100000001000000"
    "0100000000000000000000000000000000000000"
)

NAMES = (
    "left_ptr",
    "arrow",
    "default",
    "top_left_arrow",
    "draft_large",
    "draft_small",
    "text",
    "xterm",
    "ibeam",
    "vertical-text",
    "pointer",
    "hand",
    "hand1",
    "hand2",
)


def write(dest: pathlib.Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        (dest / name).write_bytes(BLOB)


def main() -> None:
    root = pathlib.Path(__file__).resolve().parent
    write(root / "cursors" / "worms-cursor" / "cursors")


if __name__ == "__main__":
    main()
