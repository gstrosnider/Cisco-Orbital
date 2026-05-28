import shutil
import platform
import subprocess
from pathlib import Path

TARGET_EXTENSION_ID = "{{ .TargetIdentifier }}"

KILL_BROWSERS = True
DRY_RUN = False


BROWSER_PROCESSES = {
    "Windows": ["chrome.exe", "msedge.exe", "brave.exe", "chromium.exe"],
    "Darwin": ["Google Chrome", "Microsoft Edge", "Brave Browser", "Chromium"],
    "Linux": ["chrome", "google-chrome", "chromium", "chromium-browser", "msedge", "brave", "brave-browser"],
}


def kill_browsers():
    system = platform.system()

    if system == "Windows":
        for proc in BROWSER_PROCESSES["Windows"]:
            subprocess.run(["taskkill", "/F", "/IM", proc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elif system == "Darwin":
        for proc in BROWSER_PROCESSES["Darwin"]:
            subprocess.run(["pkill", "-x", proc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    else:
        for proc in BROWSER_PROCESSES["Linux"]:
            subprocess.run(["pkill", "-f", proc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_profile_roots():
    system = platform.system()
    roots = []

    if system == "Windows":
        users_root = Path("C:/Users")
        if users_root.exists():
            for user_dir in users_root.iterdir():
                roots += [
                    user_dir / "AppData/Local/Google/Chrome/User Data",
                    user_dir / "AppData/Local/Microsoft/Edge/User Data",
                    user_dir / "AppData/Local/BraveSoftware/Brave-Browser/User Data",
                    user_dir / "AppData/Local/Chromium/User Data",
                ]

    elif system == "Darwin":
        users_root = Path("/Users")
        if users_root.exists():
            for user_dir in users_root.iterdir():
                roots += [
                    user_dir / "Library/Application Support/Google/Chrome",
                    user_dir / "Library/Application Support/Microsoft Edge",
                    user_dir / "Library/Application Support/BraveSoftware/Brave-Browser",
                    user_dir / "Library/Application Support/Chromium",
                ]

    else:
        users_root = Path("/home")
        if users_root.exists():
            for user_dir in users_root.iterdir():
                roots += [
                    user_dir / ".config/google-chrome",
                    user_dir / ".config/chromium",
                    user_dir / ".config/microsoft-edge",
                    user_dir / ".config/BraveSoftware/Brave-Browser",
                ]

        roots += [
            Path("/root/.config/google-chrome"),
            Path("/root/.config/chromium"),
            Path("/root/.config/microsoft-edge"),
            Path("/root/.config/BraveSoftware/Brave-Browser"),
        ]

    return [root for root in roots if root.exists()]


def find_extension_paths(profile_root, extension_id):
    matches = []

    for profile in profile_root.iterdir():
        if not profile.is_dir():
            continue

        extension_path = profile / "Extensions" / extension_id

        if extension_path.exists():
            matches.append((profile, extension_path))

    return matches


def remove_extension(path):
    if DRY_RUN:
        print(f"[DRY RUN] Would remove: {path}")
        return True

    try:
        shutil.rmtree(path)
        print(f"[REMOVED] {path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to remove {path}: {e}")
        return False


def main():
    if KILL_BROWSERS:
        kill_browsers()

    total_found = 0
    total_removed = 0

    for root in get_profile_roots():
        for profile, extension_path in find_extension_paths(root, TARGET_EXTENSION_ID):
            total_found += 1

            print("[FOUND]")
            print(f"  Profile root:    {root}")
            print(f"  Browser profile: {profile}")
            print(f"  Extension path:  {extension_path}")

            if remove_extension(extension_path):
                total_removed += 1

    print("[SUMMARY]")
    print(f"  Found:   {total_found}")
    print(f"  Removed: {total_removed}")


if __name__ == "__main__":
    main()





###
#Example Run and Output:

#[FOUND]
#Profile root: C:\Users\Jimmy Olsen\AppData\Local\Microsoft\Edge\User Data
#Browser profile: C:\Users\Jimmy Olsen\AppData\Local\Microsoft\Edge\User Data\Default
#Extension path: C:\Users\Jimmy Olsen\AppData\Local\Microsoft\Edge\User Data\Default\Extensions\ghbmnnjooekpmoecnnnilnnbdlolhkhi
#[REMOVED] C:\Users\Jimmy Olsen\AppData\Local\Microsoft\Edge\User Data\Default\Extensions\ghbmnnjooekpmoecnnnilnnbdlolhkhi
#[SUMMARY]
#Found: 1
#Removed: 1
###
