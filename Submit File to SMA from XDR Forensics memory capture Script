#Submit File to SMA from XDR Forensics Memory capture
    
import shutil
import subprocess
from pathlib import Path

filepath = Path(r"{{ .SAMPLE_FULLPATH }}")
api_key = "{{ .API_KEY }}"
notification_email = "{{ .NOTIFICATION_EMAIL }}"

if not filepath.is_file():
    raise FileNotFoundError(f"Sample file not found: {filepath}")

new_name = filepath.name
while new_name.lower().endswith((".dll", ".img")):
    if new_name.lower().endswith(".dll"):
        new_name = new_name[:-4]
    elif new_name.lower().endswith(".img"):
        new_name = new_name[:-4]

upload_copy = filepath.with_name(new_name)

shutil.copy2(filepath, upload_copy)

print(f"Original file: {filepath}")
print(f"Upload copy: {upload_copy}")

if not upload_copy.is_file():
    raise FileNotFoundError(f"Upload copy was not created: {upload_copy}")

cmd = [
    "curl",
    "--ssl-no-revoke",
    "--fail",
    "-XPOST",
    "-F", f"sample=@{upload_copy}",
    "-F", f"api_key={api_key}",
    "-F", f"email_notification={notification_email}",
    "https://panacea.threatgrid.com/api/v2/samples",
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True)

    print("Return code:", result.returncode)
    print("STDOUT:")
    print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError("curl upload failed")
finally:
    if upload_copy.exists():
        upload_copy.unlink()
        print(f"Deleted secondary copy: {upload_copy}")
