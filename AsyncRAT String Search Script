from pathlib import Path
import re

KEYWORDS = [
    "asyncrat",
    "mutex",
    "host",
    "port",
    "install",
    "pastebin",
    "keylogger",
    "stub",
    "certificate",
]

path = Path(r"{{ .FILEPATH }}")
MIN_LEN = 4

def extract_ascii_strings(data: bytes, min_len: int = 4):
    pattern = rb"[\x20-\x7e]{%d,}" % min_len
    return [m.decode("ascii", errors="ignore") for m in re.findall(pattern, data)]

def extract_utf16le_strings(data: bytes, min_len: int = 4):
    pattern = rb"(?:[\x20-\x7e]\x00){%d,}" % min_len
    matches = re.findall(pattern, data)
    results = []
    for m in matches:
        try:
            results.append(m.decode("utf-16le", errors="ignore"))
        except Exception:
            pass
    return results

def scan_file(file_path: Path):
    try:
        data = file_path.read_bytes()
    except Exception:
        return

    strings_found = extract_ascii_strings(data, MIN_LEN)
    strings_found += extract_utf16le_strings(data, MIN_LEN)

    seen = set()

    for s in strings_found:
        s_clean = s.strip()
        if not s_clean:
            continue

        lower_s = s_clean.lower()
        if any(keyword in lower_s for keyword in KEYWORDS):
            if s_clean not in seen:
                seen.add(s_clean)
                print(s_clean)

if not path.exists():
    raise FileNotFoundError(f"Target not found: {path}")

if path.is_file():
    targets = [path]
else:
    targets = [p for p in path.rglob("*") if p.is_file()]

for file_path in targets:
    scan_file(file_path)
