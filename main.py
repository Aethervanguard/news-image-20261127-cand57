#!/usr/bin/env python3
"""The Daily World — 27 November 2026.

Copies the entry image to the output directory. Stdlib only, no network,
deterministic: the same bytes are written on every run.
"""
import hashlib
import os
import shutil


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_entry(src, out_dir):
    """Copy src to out_dir/entry.png and verify it is a whole PNG under 1 MiB."""
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if _sha256(src) != _sha256(dst):
        raise SystemExit("copy mismatch: entry.png differs from source")
    size = os.path.getsize(dst)
    if size > 1048576:
        raise SystemExit(f"entry.png too large: {size} bytes")
    with open(dst, "rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("entry.png is not a PNG")
    print(f"Wrote {dst} ({size} bytes)")
    return dst


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    copy_entry(os.path.join(here, "entry.png"), out_dir)


if __name__ == "__main__":
    main()
