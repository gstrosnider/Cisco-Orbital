###Captures the memory via /proc/kcore

import os
from pathlib import Path

SRC = Path("/proc/kcore")
DST = Path("/tmp/memory.dump")
BUF = 16 * 1024 * 1024  # 16 MiB buffer

def human(n):
    for unit in ("B","KiB","MiB","GiB","TiB"):
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PiB"

if not SRC.exists():
    raise SystemExit(f"{SRC} does not exist on this system.")

with SRC.open("rb") as fin, DST.open("wb") as fout:
    while True:
        chunk = fin.read(BUF)
        if not chunk:
            break
        fout.write(chunk)

st = DST.stat()
reported_bytes = st.st_size
on_disk = getattr(st, "st_blocks", None)
if on_disk is not None:
    on_disk_bytes = on_disk * 512
    print(f"Saved to: {DST}")
    print(f"Reported size: {reported_bytes} bytes ({human(reported_bytes)})")
    print(f"On-disk size:  {on_disk_bytes} bytes ({human(on_disk_bytes)})")
else:
    print(f"Saved to: {DST} — size: {reported_bytes} bytes ({human(reported_bytes)})")
