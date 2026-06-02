#!/usr/bin/python3

import requests
import json
import os
import subprocess

SERVER = "http://192.168.51.129:8000"

LOCAL_VERSION_FILE = "/etc/ota-client/versions.json"

DEFAULT_VERSIONS = {
    "sysinfoapp": "1.0",
    "wifiapp": "1.0"
}

def load_local_versions():
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_VERSIONS.copy()

def save_local_versions(versions):
    os.makedirs("/etc/ota-client", exist_ok=True)
    with open(LOCAL_VERSION_FILE, "w") as f:
        json.dump(versions, f, indent=2)

def download_and_install(app, server_ver):
    filename = f"{app}_{server_ver}_cortexa72.ipk"
    url = f"{SERVER}/{filename}"
    tmp_path = f"/tmp/{filename}"

    print(f"  Downloading {url} ...")
    r = requests.get(url, timeout=30, stream=True)
    if r.status_code != 200:
        print(f"  ERROR: Could not download (HTTP {r.status_code})")
        return False

    with open(tmp_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"  Installing {filename} ...")
    result = subprocess.run(
        ["opkg", "install", "--force-reinstall", tmp_path],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"  SUCCESS: {app} updated to {server_ver}")
        os.remove(tmp_path)
        return True
    else:
        print(f"  ERROR: opkg install failed")
        print(result.stderr)
        return False

# ── Main ──────────────────────────────────────────

print("=================================")
print("        OTA CLIENT")
print("=================================")

local_versions = load_local_versions()

try:
    response = requests.get(f"{SERVER}/version.json", timeout=5)
    server_versions = response.json()
except Exception as e:
    print("Failed to contact OTA server:", e)
    exit(1)

print("\nChecking updates...\n")

updated_any = False

for app in local_versions:
    local_ver = local_versions[app]
    server_ver = server_versions.get(app, local_ver)

    print(f"{app}")
    print(f"  Local  : {local_ver}")
    print(f"  Server : {server_ver}")

    if local_ver != server_ver:
        print("  UPDATE AVAILABLE")
        choice = input("  Update now? [y/n]: ").strip().lower()
        if choice == "y":
            success = download_and_install(app, server_ver)
            if success:
                local_versions[app] = server_ver
                updated_any = True
        else:
            print("  Skipped.")
    else:
        print("  UP TO DATE")
    print()

if updated_any:
    save_local_versions(local_versions)
    print("Local version file updated.")

print("Done.")
