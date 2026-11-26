#!/usr/bin/env python3
"""Write the fortune-cookie entry to /output/entry.txt.

Reads the entry text from the entry.txt file shipped beside this script,
writes it to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output), then verifies
the output by size and sha256 so a truncated or corrupted write is caught.
Standard library only; deterministic.
"""

import hashlib
import os
import sys
from pathlib import Path

ENTRY_TEXT = (
    "You are now 100% in cash. "
    "The market has officially run out of ways to hurt you."
)


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"

    # The shipped entry.txt is the source of truth; ENTRY_TEXT must match it.
    here = Path(__file__).resolve().parent
    shipped = (here / "entry.txt").read_text(encoding="utf-8")
    if shipped != ENTRY_TEXT:
        print("error: ENTRY_TEXT does not match shipped entry.txt", file=sys.stderr)
        return 1

    data = ENTRY_TEXT.encode("utf-8")
    out_path.write_bytes(data)

    # Verify: size and sha256 of what was actually written.
    written = out_path.read_bytes()
    if written != data:
        print("error: verification failed, output differs", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {out_path} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
