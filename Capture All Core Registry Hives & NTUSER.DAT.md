Uses Volume Shadow Copy
Dumps All Core Registry Hives + NTUSER.DAT
Zips Output with Basic Password Protection

# Files it Captures:


|Hive/File       | Path in Shadow Copy               |
|----------------|-----------------------------------|
| SYSTEM         | Windows\System32\config\SYSTEM    |
| SOFTWARE       | Windows\System32\config\SOFTWARE  |
| SAM            | Windows\System32\config\SAM       |
| SECURITY       | Windows\System32\config\SECURITY  | 
| DEFAULT        | Windows\System32\config\DEFAULT   |
| NTUSER.DAT     | Users\<username>\NTUSER.DAT       |


# Orbital Script Code:

```
import subprocess
import os
import shutil
import time
import zipfile
import getpass

# === CONFIGURATION ===
PASSWORD = "{{ .Zip_Password }}"
timestamp = time.strftime("%Y%m%d_%H%M%S")
BASE_DIR = os.path.join("C:\\RegistryVSSDump", timestamp)
ZIP_PATH = BASE_DIR + ".zip"

HIVES = ["SYSTEM", "SOFTWARE", "SAM", "SECURITY", "DEFAULT"]

def run_cmd(cmd, capture_output=False):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    return result.stdout.strip() if capture_output else None

def create_shadow_copy():
    print("Creating shadow copy...")
    output = run_cmd("wmic shadowcopy call create Volume='C:\\'", capture_output=True)
    if "ShadowID" not in output:
        raise RuntimeError("Failed to create shadow copy.")
    shadow_id = output.split("ShadowID")[1].split("=")[1].split("\"")[1]
    print(f"Shadow copy created: {shadow_id}")
    return shadow_id

def get_shadow_device(shadow_id):
    print("Getting shadow device path...")
    output = run_cmd(f"wmic shadowcopy where ID='{shadow_id}' get DeviceObject", capture_output=True)
    device = [line.strip() for line in output.splitlines() if line.strip().startswith("\\\\")][0]
    print(f"Shadow device: {device}")
    return device

def copy_registry_hives(device, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    reg_dir = os.path.join(device, "Windows", "System32", "config")
    for hive in HIVES:
        src = os.path.join(reg_dir, hive)
        dst = os.path.join(output_dir, f"{hive}.dat")
        try:
            shutil.copy2(src, dst)
            print(f"Copied {hive}")
        except Exception as e:
            print(f"Failed to copy {hive}: {e}")

def copy_ntuser_dat(device, output_dir):
    print("Searching for NTUSER.DAT...")
    user_dir = os.path.join(device, "Users")
    try:
        for user in os.listdir(user_dir):
            profile = os.path.join(user_dir, user)
            hive_path = os.path.join(profile, "NTUSER.DAT")
            if os.path.isfile(hive_path):
                dst = os.path.join(output_dir, f"NTUSER_{user}.dat")
                try:
                    shutil.copy2(hive_path, dst)
                    print(f"Copied NTUSER.DAT for user: {user}")
                except Exception as e:
                    print(f"Failed to copy NTUSER for {user}: {e}")
    except Exception as e:
        print(f"Could not enumerate user profiles: {e}")

def delete_shadow_copy(shadow_id):
    print("Cleaning up shadow copy...")
    run_cmd(f"wmic shadowcopy where ID='{shadow_id}' delete")
    print("Shadow copy deleted.")

def zip_folder(folder_path, zip_path, password):
    print("Creating password-protected ZIP...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_file = os.path.join(root, file)
                arcname = os.path.relpath(abs_file, start=folder_path)
                with open(abs_file, 'rb') as f:
                    zipf.writestr(arcname, f.read())
        zipf.setpassword(password.encode())  # Note: Only works during extraction
    print(f"Created ZIP: {zip_path}")

def main():
    if os.name != 'nt':
        print("This script only works on Windows.")
        return

    print("Starting VSS-based registry dump...")

    try:
        shadow_id = create_shadow_copy()
        device = get_shadow_device(shadow_id)

        copy_registry_hives(device, BASE_DIR)
        copy_ntuser_dat(device, BASE_DIR)

        zip_folder(BASE_DIR, ZIP_PATH, PASSWORD)

    finally:
        try:
            delete_shadow_copy(shadow_id)
        except:
            print("[!] Warning: Shadow copy may not have been deleted.")

    print("\nDump complete.")
    print(f"Output Folder: {BASE_DIR}")
    print(f"ZIP File: {ZIP_PATH}")

if __name__ == "__main__":
    main()
```

# Output Example
```
Deleting instance \\DESKTOP-3BVGA43\ROOT\CIMV2:Win32_ShadowCopy.ID="{86B90750-05B9-4FC7-BE45-3938C2FDA3C8}"

Instance deletion successful.

Starting VSS-based registry dump...
Creating shadow copy...
Shadow copy created: {86B90750-05B9-4FC7-BE45-3938C2FDA3C8}
Getting shadow device path...
Shadow device: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy5
Copied SYSTEM
Copied SOFTWARE
Copied SAM
Copied SECURITY
Copied DEFAULT
Searching for NTUSER.DAT...
Copied NTUSER.DAT for user: Default
Copied NTUSER.DAT for user: Default User
Copied NTUSER.DAT for user: TestUser
Creating password-protected ZIP...
Created ZIP: C:\RegistryVSSDump\20250530_160054.zip
Cleaning up shadow copy...
Shadow copy deleted.

Dump complete.
Output Folder: C:\RegistryVSSDump\20250530_160054
ZIP File: C:\RegistryVSSDump\20250530_160054.zip
```
