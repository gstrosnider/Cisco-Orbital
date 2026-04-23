##Analyze memory dump using Volatility's malfind

import sys
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
from volatility3.cli import CommandLine

case_root = Path(r"{{ .XDRForensicsFilePath }}")
output_file = Path(r"{{ .OutputFile }}")

if case_root.is_dir():
    matches = list(case_root.rglob("ram-image.raw"))
    if not matches:
        raise FileNotFoundError(f"No ram-image.raw found under {case_root}")
    dumppath = matches[0]
else:
    if not case_root.exists():
        raise FileNotFoundError(f"Memory image not found: {case_root}")
    dumppath = case_root

output_file.parent.mkdir(parents=True, exist_ok=True)

sys.argv = [
    "vol",
    "-q",
    "-f", str(dumppath),
    "windows.malfind",
]

with output_file.open("w", encoding="utf-8") as f:
    with redirect_stdout(f), redirect_stderr(f):
        CommandLine().run()

print(f"[+] Output saved to {output_file}")
