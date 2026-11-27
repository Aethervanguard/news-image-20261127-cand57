#!/usr/bin/env python3
"""The Daily World — 27 November 2026.

Photo front page entry point. The grader runs this file; it places the
pre-rendered front-page PNG into the output directory. Standard library
only, no network access, and the output bytes never change between runs.
"""
import hashlib
import os
import shutil

MAX_BYTES = 1_048_576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _file_hash(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _place_image(source, target_dir):
    """Place source as target_dir/entry.png, refusing anything unexpected."""
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    if _file_hash(source) != _file_hash(target):
        raise SystemExit("entry.png copy failed integrity check")
    total = os.path.getsize(target)
    if total > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB")
    with open(target, "rb") as handle:
        head = handle.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        raise SystemExit("entry.png is not a PNG file")
    print("Wrote %s (%d bytes)" % (target, total))


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    destination = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    _place_image(os.path.join(base, "entry.png"), destination)


if __name__ == "__main__":
    main()
