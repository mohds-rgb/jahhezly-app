# Release Plan

## Current portfolio release

`0.2.0` — Portfolio Release Candidate

This release is intended as a reviewable GitHub engineering artifact, not as a production deployment.

## Release identifiers

A future distributable build must record:

```text
version
build number
Git commit
build timestamp
API version
backend schema version
mobile schema version
platform target
release channel
```

## Current state

```text
Source implementation     IMPLEMENTED
Backend tests              TESTED
Migration verification     TESTED
Repository checks          VERIFIED
Mobile/device validation   NOT VERIFIED
PostgreSQL runtime         NOT VERIFIED
Production deployment      NOT CLAIMED
```

## Before a real mobile release

Run on a developer workstation:

1. `flutter analyze`
2. `flutter test`
3. Android build and installation on a representative device
4. iOS build and installation on a representative device
5. offline catalog/cart/restart verification
6. queued order recovery verification
7. notification permission and interaction verification
8. security/configuration review
9. release artifact hashing
10. compatibility review against the chosen API window

Do not mark an artifact `VERIFIED` without recording the actual command and result.
