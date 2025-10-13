# CHANGELOG

<!-- version list -->

## v0.5.0 (2025-10-13)

### Bug Fixes

- Properly show read-all/write-all permissions
  ([#33](https://github.com/watermarkhu/mkdocstrings-github/pull/33),
  [`5f5e792`](https://github.com/watermarkhu/mkdocstrings-github/commit/5f5e7921fd326bbcdec903101107c6128dab5dbf))

### Documentation

- Better docs with actions/checkout example
  ([#33](https://github.com/watermarkhu/mkdocstrings-github/pull/33),
  [`5f5e792`](https://github.com/watermarkhu/mkdocstrings-github/commit/5f5e7921fd326bbcdec903101107c6128dab5dbf))

### Features

- Move signature repository name to local options
  ([#33](https://github.com/watermarkhu/mkdocstrings-github/pull/33),
  [`5f5e792`](https://github.com/watermarkhu/mkdocstrings-github/commit/5f5e7921fd326bbcdec903101107c6128dab5dbf))


## v0.4.5 (2025-10-13)

### Refactoring

- Show annotation in stead of empty
  ([#32](https://github.com/watermarkhu/mkdocstrings-github/pull/32),
  [`46942af`](https://github.com/watermarkhu/mkdocstrings-github/commit/46942af6c6c2794830738749909edd39ea2ca204))

- Show annotation instead of empty
  ([#32](https://github.com/watermarkhu/mkdocstrings-github/pull/32),
  [`46942af`](https://github.com/watermarkhu/mkdocstrings-github/commit/46942af6c6c2794830738749909edd39ea2ca204))


## v0.4.4 (2025-10-13)

### Bug Fixes

- **templates**: Hide signature sections properly
  ([#31](https://github.com/watermarkhu/mkdocstrings-github/pull/31),
  [`86d9628`](https://github.com/watermarkhu/mkdocstrings-github/commit/86d9628770ab235280ffc65434009355946b7d0c))


## v0.4.3 (2025-10-12)

### Bug Fixes

- Hide secrets and inputs from signature if there are none
  ([#30](https://github.com/watermarkhu/mkdocstrings-github/pull/30),
  [`f9831f6`](https://github.com/watermarkhu/mkdocstrings-github/commit/f9831f648b8eeed287f35843a1d15c7f845c1bb0))

### Continuous Integration

- More tests ([#30](https://github.com/watermarkhu/mkdocstrings-github/pull/30),
  [`f9831f6`](https://github.com/watermarkhu/mkdocstrings-github/commit/f9831f648b8eeed287f35843a1d15c7f845c1bb0))

### Performance Improvements

- Use GITHUB_REPOSITORY env var in GitHub Actions
  ([#30](https://github.com/watermarkhu/mkdocstrings-github/pull/30),
  [`f9831f6`](https://github.com/watermarkhu/mkdocstrings-github/commit/f9831f648b8eeed287f35843a1d15c7f845c1bb0))


## v0.4.2 (2025-10-08)

### Bug Fixes

- Better package tag ordering ([#28](https://github.com/watermarkhu/mkdocstrings-github/pull/28),
  [`10dc87a`](https://github.com/watermarkhu/mkdocstrings-github/commit/10dc87a001908af6522320a5248ce4c988e441a3))


## v0.4.1 (2025-10-08)

### Bug Fixes

- Tag ordering ([#27](https://github.com/watermarkhu/mkdocstrings-github/pull/27),
  [`76256f5`](https://github.com/watermarkhu/mkdocstrings-github/commit/76256f52bbd53be825ba0a0576d7cb6a6da54d3a))

### Documentation

- Update docs ([#26](https://github.com/watermarkhu/mkdocstrings-github/pull/26),
  [`96f650f`](https://github.com/watermarkhu/mkdocstrings-github/commit/96f650f1d4af5b5d6da4704e7b2184e4016f3a39))


## v0.4.0 (2025-10-08)

### Continuous Integration

- **deps**: Update actions/checkout action to v5
  ([#22](https://github.com/watermarkhu/mkdocstrings-github/pull/22),
  [`fc56971`](https://github.com/watermarkhu/mkdocstrings-github/commit/fc569719b4387f11119de588d2f67f1daa09c233))

- **deps**: Update astral-sh/setup-uv action to v7
  ([#24](https://github.com/watermarkhu/mkdocstrings-github/pull/24),
  [`a07de53`](https://github.com/watermarkhu/mkdocstrings-github/commit/a07de53b318859a365215730c2c09d0d5fdcf5b1))

### Features

- Get releases using tags ([#25](https://github.com/watermarkhu/mkdocstrings-github/pull/25),
  [`25ea11d`](https://github.com/watermarkhu/mkdocstrings-github/commit/25ea11d8c0f92a1e49f8b35b60456259e4e0ec7b))


## v0.3.0 (2025-10-07)

### Bug Fixes

- Prek configuration with local uv
  ([#20](https://github.com/watermarkhu/mkdocstrings-github/pull/20),
  [`0d53c40`](https://github.com/watermarkhu/mkdocstrings-github/commit/0d53c4029fc0f2e30f4f223b6d81221236254832))

### Build System

- **deps**: Update dependency ruff to ~=0.14.0
  ([#21](https://github.com/watermarkhu/mkdocstrings-github/pull/21),
  [`f87cf24`](https://github.com/watermarkhu/mkdocstrings-github/commit/f87cf2485121f4056279ce06ed721e02fc475f1b))

### Continuous Integration

- Add codecov ([#20](https://github.com/watermarkhu/mkdocstrings-github/pull/20),
  [`0d53c40`](https://github.com/watermarkhu/mkdocstrings-github/commit/0d53c4029fc0f2e30f4f223b6d81221236254832))

- **deps**: Update peter-evans/create-or-update-comment action to v5
  ([#19](https://github.com/watermarkhu/mkdocstrings-github/pull/19),
  [`8135a2b`](https://github.com/watermarkhu/mkdocstrings-github/commit/8135a2bff69a41bde0676b991145ff089563bf7b))

### Features

- Hide default and section if non are available
  ([#20](https://github.com/watermarkhu/mkdocstrings-github/pull/20),
  [`0d53c40`](https://github.com/watermarkhu/mkdocstrings-github/commit/0d53c4029fc0f2e30f4f223b6d81221236254832))

- Hide default and section if non are available.
  ([#20](https://github.com/watermarkhu/mkdocstrings-github/pull/20),
  [`0d53c40`](https://github.com/watermarkhu/mkdocstrings-github/commit/0d53c4029fc0f2e30f4f223b6d81221236254832))


## v0.2.6 (2025-10-02)

### Bug Fixes

- Empty workflow_call ([#18](https://github.com/watermarkhu/mkdocstrings-github/pull/18),
  [`368b9b5`](https://github.com/watermarkhu/mkdocstrings-github/commit/368b9b5097d6d0c061cb9addbfc9fc721a16dea7))

### Continuous Integration

- **deps**: Update peter-evans/find-comment action to v4
  ([#17](https://github.com/watermarkhu/mkdocstrings-github/pull/17),
  [`8e2375d`](https://github.com/watermarkhu/mkdocstrings-github/commit/8e2375d1df0a9883c9a365dfc5b2563997fb1f70))


## v0.2.5 (2025-09-29)

### Bug Fixes

- No repo set ([#16](https://github.com/watermarkhu/mkdocstrings-github/pull/16),
  [`554d230`](https://github.com/watermarkhu/mkdocstrings-github/commit/554d230a3c8da0bee86a2c8b2805c873852d6bfd))

### Documentation

- Small fix ([#15](https://github.com/watermarkhu/mkdocstrings-github/pull/15),
  [`22c6693`](https://github.com/watermarkhu/mkdocstrings-github/commit/22c669395cce94b315ab08434fdc4e7ba167f7a5))


## v0.2.4 (2025-09-29)

### Bug Fixes

- Allow setting hostname ([#14](https://github.com/watermarkhu/mkdocstrings-github/pull/14),
  [`4676e57`](https://github.com/watermarkhu/mkdocstrings-github/commit/4676e57cda03b8a52ae6facf4a28f3dde9adb365))

- Set hostname ([#14](https://github.com/watermarkhu/mkdocstrings-github/pull/14),
  [`4676e57`](https://github.com/watermarkhu/mkdocstrings-github/commit/4676e57cda03b8a52ae6facf4a28f3dde9adb365))


## v0.2.3 (2025-09-29)

### Bug Fixes

- Default host ([#13](https://github.com/watermarkhu/mkdocstrings-github/pull/13),
  [`8ac9b06`](https://github.com/watermarkhu/mkdocstrings-github/commit/8ac9b062e53b47e27cc1adad6c206087d8a7da1a))


## v0.2.2 (2025-09-29)

### Bug Fixes

- Get GH_TOKEN ([#12](https://github.com/watermarkhu/mkdocstrings-github/pull/12),
  [`3c449ea`](https://github.com/watermarkhu/mkdocstrings-github/commit/3c449ea0bfeaac96667d7d31b668d25921279bd6))


## v0.2.1 (2025-09-29)

### Bug Fixes

- GitHub Enterprise with GH_HOST ([#11](https://github.com/watermarkhu/mkdocstrings-github/pull/11),
  [`4f59dc0`](https://github.com/watermarkhu/mkdocstrings-github/commit/4f59dc07eb1f564d31431e4f3bf2e6fb1bcdfeb6))

### Documentation

- Update docs ([#10](https://github.com/watermarkhu/mkdocstrings-github/pull/10),
  [`3be05f5`](https://github.com/watermarkhu/mkdocstrings-github/commit/3be05f57605fbf12ab9c1ea8583775e1e47b25f2))


## v0.2.0 (2025-09-28)

### Features

- Cross-linking ([#9](https://github.com/watermarkhu/mkdocstrings-github/pull/9),
  [`6bcf229`](https://github.com/watermarkhu/mkdocstrings-github/commit/6bcf229ad97702a44ba68ceb135ffd4b53208339))


## v0.1.0 (2025-09-28)

- Initial Release
