# AGENTS.md — omnipha/images

Purpose: per-device experimental image definitions + validation-only CI; no public releases exist.

## Layout
- `devices/<codename>/` — image definition (kernel branch, ports packages, profile, partition layout)
- `.github/workflows/` — validation-only workflow (one matrix job per device); no build or upload

## Conventions
- Adding a device here requires a `device.yaml` in omnipha/ports first.
- No tag can be treated as a release until `BUILD-MANIFEST.md` and the ports release evidence gate are fulfilled; never flash from partition metadata.
- Builder CI mode is not implemented; never claim that a green validation workflow created a rootfs or boot image.
- Never commit SSH private keys, firmware blobs or device dumps. Refer to BUILD-MANIFEST.md for required pinned inputs and output checksums.

## Facts
- First target: xiaomi-laurel, profile server, kernel omnipha/linux-sm61x5 branch omnipha.
