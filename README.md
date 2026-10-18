# omnipha/images

Flashable image definitions and release builds for Omnipha devices. Every
device folder defines which kernel (omnipha/linux-<soc>), which packages
(omnipha/ports) and which profile (server / agent-host / console-ui) go into
the image. GitHub Actions builds and publishes them as releases.

## Profiles
- `server` — headless: sshd (key-only), no lockscreen, no UI. Minimal attack surface.
- `agent-host` — server + container runtime + Node/Python toolchains (Claude Code, Codex, OpenClaw, Hermes ready)
- `console-ui` — server + console UI on the phone display (Weston/Phosh without lockscreen)

## Releases
Built from tags `device/<codename>/<version>`. Images flash via fastboot; SSH
host keys are generated on first boot, the authorized key is baked in at build
time (CI uses a dedicated build key; pass your own via builder `--ssh-pubkey`).

## Status
Bootstrap. First build target: xiaomi-laurel (server profile), pending builder
CI mode (see omnipha/builder issues).

## License
MIT for build definitions; produced images combine GPL and proprietary
firmware (device firmware is extracted at build time, never distributed inside
this repo).
