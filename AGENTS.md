# AGENTS.md — omnipha/images

Purpose: per-device image definitions + CI that publishes flashable releases.

## Layout
- `devices/<codename>/` — image definition (kernel branch, ports packages, profile, partition layout)
- `.github/workflows/` — build workflows (one matrix job per device)

## Conventions
- Adding a device here requires a `device.yaml` in omnipha/ports first.
- Tag format for releases: `device/<codename>/<version>`.
- CI builds must run in non-interactive mode (builder --non-interactive).
- Never commit SSH private keys. Public keys only, and only CI build keys.

## Facts
- First target: xiaomi-laurel, profile server, kernel omnipha/linux-sm61x5 branch omnipha.
