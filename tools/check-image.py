#!/usr/bin/env python3
"""Validate an Omnipha image definition. Non-interactive, no prompts.

This does not build an image. omnipha/builder has no --non-interactive,
--profile or --ssh-pubkey mode yet, so no rootfs or boot image is produced
here. The command checks devices/<codename>/image.yaml for internal
consistency and, when --ports is given, against the device package in an
omnipha/ports checkout. It prints a sha256 of the canonical definition so a
reviewer can confirm exactly which definition was checked.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("pyyaml is required: pip install pyyaml")

PROFILES = ("server", "agent-host", "console-ui")
FLASH_METHODS = ("fastboot",)
USERDATA_FILESYSTEMS = ("ext4", "f2fs", "btrfs")
REQUIRED = ("device", "soc", "kernel", "profile", "packages", "firmware", "flash")


def fail(message: str) -> None:
    sys.exit(f"error: {message}")


def load_definition(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        fail(f"{path}: invalid YAML: {exc}")
    if not isinstance(data, dict):
        fail(f"{path}: image definition must be a mapping")
    return data


def check(data: dict, path: Path, ports: Path | None) -> None:
    missing = [key for key in REQUIRED if key not in data]
    if missing:
        fail(f"{path}: missing keys: {', '.join(missing)}")

    device = data["device"]
    if not isinstance(device, str) or not device:
        fail(f"{path}: device must be a non-empty string")
    if path.parent.name != device:
        fail(f"{path}: directory {path.parent.name!r} != device {device!r}")

    soc = data["soc"]
    if not isinstance(soc, str) or not soc:
        fail(f"{path}: soc must be a non-empty string")

    kernel = data["kernel"]
    if not isinstance(kernel, dict) or not kernel.get("repo") or not kernel.get("branch"):
        fail(f"{path}: kernel needs repo and branch")

    if data["profile"] not in PROFILES:
        fail(f"{path}: profile {data['profile']!r} not in {PROFILES}")

    packages = data["packages"]
    if not isinstance(packages, list) or not packages:
        fail(f"{path}: packages must be a non-empty list")
    names = [str(p).split()[0] for p in packages]
    if f"device-{device}" not in names:
        fail(f"{path}: packages must include device-{device}")
    if "openssh" not in names:
        fail(f"{path}: profile server requires openssh (sshd, key-only)")

    firmware = data["firmware"]
    if not isinstance(firmware, dict) or not firmware.get("source"):
        fail(f"{path}: firmware needs a source")

    flash = data["flash"]
    if not isinstance(flash, dict) or flash.get("method") not in FLASH_METHODS:
        fail(f"{path}: flash.method must be one of {FLASH_METHODS}")
    partitions = flash.get("partitions")
    if not isinstance(partitions, list) or "boot" not in partitions:
        fail(f"{path}: flash.partitions must list at least boot")
    userdata = flash.get("userdata")
    if userdata is not None:
        filesystem = userdata.get("filesystem") if isinstance(userdata, dict) else None
        if filesystem not in USERDATA_FILESYSTEMS:
            fail(f"{path}: userdata filesystem {filesystem!r} not in {USERDATA_FILESYSTEMS}")

    print(f"ok: {device} soc={soc} profile={data['profile']} packages={len(names)}")
    print(f"ok: flash {flash['method']} partitions={','.join(partitions)}")

    if ports is None:
        return
    device_dir = ports / "devices" / device
    device_yaml = device_dir / "device.yaml"
    if not device_yaml.is_file():
        fail(f"{path}: no device package at {device_dir} (device.yaml required)")
    port = yaml.safe_load(device_yaml.read_text())
    if port.get("codename") != device:
        fail(f"{device_yaml}: codename {port.get('codename')!r} != {device!r}")
    if port.get("soc") != soc:
        fail(f"{device_yaml}: soc {port.get('soc')!r} != image soc {soc!r}")
    if not (device_dir / "APKBUILD").is_file():
        fail(f"{device_dir}: missing APKBUILD")
    print(f"ok: ports device.yaml + APKBUILD present, soc matches")


def digest(data: dict) -> str:
    body = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(body).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("definition", type=Path)
    parser.add_argument("--ports", type=Path, help="omnipha/ports checkout")
    args = parser.parse_args()
    if not args.definition.is_file():
        fail(f"not a file: {args.definition}")
    data = load_definition(args.definition)
    check(data, args.definition, args.ports)
    print(f"definition-sha256: {digest(data)}")


if __name__ == "__main__":
    main()
