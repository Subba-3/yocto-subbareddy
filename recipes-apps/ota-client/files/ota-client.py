#!/usr/bin/python3

import json
import os
import subprocess
import urllib.request

SERVER = "https://subbareddy-ota.s3.amazonaws.com"

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


def download_and_install(app, server_ver, filename):

    url = f"{SERVER}/packages/{filename}"
    tmp_path = f"/tmp/{filename}"

    print(f"  Downloading {url} ...")

    try:
        urllib.request.urlretrieve(url, tmp_path)
    except Exception as e:
        print(f"  ERROR: Could not download: {e}")
        return False

    print("  Updating package feed ...")

    subprocess.run(
        ["opkg", "update"],
        capture_output=True,
        text=True
    )

    print(f"  Installing {filename} ...")

    result = subprocess.run(
        [
            "opkg",
            "install",
            "--force-reinstall",
            tmp_path
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"  SUCCESS: {app} updated to {server_ver}")

        try:
            os.remove(tmp_path)
        except:
            pass

        return True

    print("  ERROR: opkg install failed")
    print(result.stderr)

    return False


# --------------------------------------------------
# Main
# --------------------------------------------------

print("=================================")
print("         OTA CLIENT")
print("=================================")

local_versions = load_local_versions()

try:
    with urllib.request.urlopen(
        f"{SERVER}/version.json",
        timeout=5
    ) as r:
        server_versions = json.loads(r.read())

except Exception as e:
    print("Failed to contact OTA server:", e)
    exit(1)

print("\nChecking updates...\n")

updated_any = False

for app in server_versions:

    local_ver = local_versions.get(app, "none")

    server_ver = server_versions[app]["version"]
    filename = server_versions[app]["filename"]

    print(f"{app}")
    print(f"  Local  : {local_ver}")
    print(f"  Server : {server_ver}")

    if local_ver != server_ver:

        print("  UPDATE AVAILABLE")

        choice = input(
            "  Update now? [y/n]: "
        ).strip().lower()

        if choice == "y":

            success = download_and_install(
                app,
                server_ver,
                filename
            )

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
