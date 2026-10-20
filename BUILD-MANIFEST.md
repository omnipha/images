# Image build provenance and release contract

Omnipha image definitions are **not** installable images. The current
`.github/workflows/build.yml` validates YAML against a pinned ports checkout;
it does not build, sign, upload or release an image. A successful green check
is not evidence that Omnipha boots. No device may be declared installable by
linking the definition's SHA-256 printed by `tools/check-image.py`.

## Publish only after a real build exists

A future builder/CI implementation must produce a public, immutable artifact
and a manifest for each device and profile. The manifest must name:

- canonical `ports` device ID and exact commit, `images` commit and the image
  definition SHA-256, `builder` commit, profile, package version/source hashes,
  kernel source commit and applied patch stack;
- output image name, size and SHA-256, toolchain/version and build-run URL;
- public references for firmware **provenance only**, never proprietary blobs,
  partition dumps, SSH private keys or personally identifying device data.

Publication must fail closed if any referenced source or artifact cannot be
retrieved or the SHA-256 does not match. A build manifest alone is **not** a
release gate: `ports/devices/<id>/device.yaml` sets `release.status: testing`
or `official` only after an immutable artifact URL, SHA-256, manifest URL,
reproducible CI run, device-specific flashing **and rollback** documentation
and a dated, physical boot/network/key-only SSH test have been reviewed by a
named hardware tester. `official` additionally needs a maintained device and
named release owner. See [the ports contribution contract](https://github.com/omnipha/ports/blob/main/CONTRIBUTING.md).

Never execute `image.yaml` partition metadata as a flashing procedure.
Nothing Phone (3a) Pro uses header-v4 A/B boot chains, and experimental
partition metadata is not a verified install recipe. No GitHub Action here
may publish releases until the builder runs noninteractively and produces a
verifiable manifest and images. Tracked blockers: [builder#1](https://github.com/omnipha/builder/issues/1)
and [nothing image#1](https://github.com/omnipha/images/issues/1).
