#Extract XDR Foresnics Memory Dump

import os
import re
import zipfile
import tarfile
import gzip
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(r"{{ .XDRForensicsCollectionPath }}")
#XDR Forensics Windows Case Directory:  C:\Cisco\Cisco XDR Forensics\Cases
#XDR Forensics Linux Case Directory: /opt/cisco/cisco xdr forensics/Cases

# Naming convention:
NAME_PATTERN = re.compile(r"^\d{14}-[A-Za-z0-9._-]+")

# Supported archive extensions
ARCHIVE_EXTENSIONS = [
    ".zip",
    ".7z",      # placeholder unless py7zr is installed
    ".tar",
    ".tgz",
    ".gz",
    ".tar.gz"
]

def is_target_archive(path: Path) -> bool:
    name = path.name.lower()
    stem_match = NAME_PATTERN.match(path.stem) or NAME_PATTERN.match(path.name)

    return path.is_file() and stem_match and any(
        name.endswith(ext) for ext in ARCHIVE_EXTENSIONS
    )

def is_archive(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(ext) for ext in ARCHIVE_EXTENSIONS)

def extract_zip(archive_path: Path, extract_to: Path):
    with zipfile.ZipFile(archive_path, 'r') as zf:
        zf.extractall(extract_to)

def extract_tar(archive_path: Path, extract_to: Path):
    with tarfile.open(archive_path, 'r:*') as tf:
        tf.extractall(extract_to)

def extract_gz(archive_path: Path, extract_to: Path):
    output_file = extract_to / archive_path.stem
    with gzip.open(archive_path, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def extract_7z(archive_path: Path, extract_to: Path):
    try:
        import py7zr
    except ImportError:
        print(f"[!] Skipping 7z archive (py7zr not installed): {archive_path}")
        return

    with py7zr.SevenZipFile(archive_path, mode='r') as z:
        z.extractall(path=extract_to)

def extract_archive(archive_path: Path, extract_to: Path):
    name = archive_path.name.lower()

    print(f"[+] Extracting: {archive_path}")
    extract_to.mkdir(parents=True, exist_ok=True)

    if name.endswith(".zip"):
        extract_zip(archive_path, extract_to)
    elif name.endswith(".tar.gz") or name.endswith(".tgz") or name.endswith(".tar"):
        extract_tar(archive_path, extract_to)
    elif name.endswith(".gz"):
        extract_gz(archive_path, extract_to)
    elif name.endswith(".7z"):
        extract_7z(archive_path, extract_to)
    else:
        print(f"[!] Unsupported archive type: {archive_path}")

def recursive_extract(start_dir: Path):
    processed = set()
    found_new = True

    while found_new:
        found_new = False

        for root, _, files in os.walk(start_dir):
            for file in files:
                file_path = Path(root) / file

                if file_path in processed:
                    continue

                if is_archive(file_path):
                    extract_folder = file_path.parent / f"{file_path.stem}_extracted"

                    try:
                        extract_archive(file_path, extract_folder)
                        processed.add(file_path)
                        found_new = True
                    except Exception as e:
                        print(f"[!] Failed to extract {file_path}: {e}")

def main():
    if not BASE_DIR.exists():
        print(f"[!] Directory does not exist: {BASE_DIR}")
        return

    matched = False

    for item in BASE_DIR.iterdir():
        if is_target_archive(item):
            matched = True
            extract_root = item.parent / f"{item.stem}_extracted"

            try:
                extract_archive(item, extract_root)
                recursive_extract(extract_root)
            except Exception as e:
                print(f"[!] Failed to process {item}: {e}")

    if not matched:
        print("[!] No matching archives found.")

if __name__ == "__main__":
    main()
