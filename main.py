# news-image-20261122 entry (Python 3.13, standard library only): the image
# is entry.png beside this file, and the program copies it to
# /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB
# and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
DEST = OUT_DIR / "entry.png"

OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, DEST)

original = SOURCE.read_bytes()
copied = DEST.read_bytes()
if len(original) > 1048576:
    raise SystemExit(f"entry.png is {len(original)} bytes, over the 1 MiB cap")
if original[:8] != b"\x89PNG\r\n\x1a\n" or original[12:16] != b"IHDR":
    raise SystemExit("entry.png is not a PNG file")
if not original.rstrip(b"\x00").endswith(b"IEND\xaeB`\x82"):
    raise SystemExit("entry.png is truncated: no IEND chunk at the end")
width = int.from_bytes(original[16:20], "big")
height = int.from_bytes(original[20:24], "big")
if width > 1024 or height > 1024:
    raise SystemExit(f"entry.png is {width}x{height}, over the 1024x1024 cap")
if original != copied:
    raise SystemExit("copy mismatch: output differs from entry.png")
digest = hashlib.sha256(copied).hexdigest()
print(f"wrote {DEST} ({len(copied)} bytes, sha256 {digest})")
