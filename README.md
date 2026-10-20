# omnipha/images

Experimental image definitions for Omnipha devices. Each device folder
specifies an intended kernel source, `ports` packages and profile. **There are
no public Omnipha image artifacts yet.** GitHub Actions currently validates
these definitions only; it does not build or publish images. The canonical
availability status is in [ports/DEVICES.md](https://github.com/omnipha/ports/blob/main/DEVICES.md).

## Profiles
- `server` — headless: sshd (key-only), no lockscreen, no UI. Minimal attack surface.
- `agent-host` — server + container runtime + Node/Python toolchains (Claude Code, Codex, OpenClaw, Hermes ready)
- `console-ui` — server + console UI on the phone display (Weston/Phosh without lockscreen)

## Releases and provenance

[BUILD-MANIFEST.md](BUILD-MANIFEST.md) defines the artifact-input provenance
and the device's physical release gate. The previously proposed tag and
SSH-key flows are **not implemented**; this repository publishes no image.
`image.yaml` flash fields are *metadata*, not safe user instructions. Once a
real builder creates validated images, the matching `ports` release entry
must link a SHA-256-verified artifact, manifest and device-specific rollback.

## Status
First planned build target: xiaomi-laurel (server profile). Nothing-asteroids
has an experimental definition and no successful Omnipha boot. Both remain
`unreleased` in `ports`. Builder's noninteractive CI mode is still blocked
(see [builder#1](https://github.com/omnipha/builder/issues/1)). A green
"Validate image definitions" workflow does **not** make an image.

## License
MIT for build definitions; future produced images may combine GPL and device firmware obtained
by the user under its own licensing; no firmware is distributed in this repo.
