# `docs/vendored/` -- snapshots of documents whose home is outside this repo

**Do not edit anything in this directory.** Every file here is a byte-for-byte copy of a
document that lives somewhere else. Editing the copy forks it silently: the canonical
document keeps being updated, this one stops, and nothing announces the divergence.

To change a vendored document, edit it at its home, then re-copy it here and update the
hash below in the same commit.

## Why these are copied rather than pointed at

A pointer to a path outside the repo is what created the gap this directory closes.
PLA-256 committed a 20,168-pair register frame and two draws, and the standard those draws
are read under lived only at `~/Documents/plant-project/05-methodology/current/`. Nothing
in the repo named it. A reader a year out would find 40 unclassified pairs and no rule to
read them under -- and a path in a commit message is not a document, because the machine
holding that path is not part of the repo.

Vendoring is deliberately byte-for-byte, with no added banner, so the copy's hash can be
compared against its source and drift is a measurement rather than a judgment call.

## The register

| file | home | source sha256 | snapshot taken |
| -- | -- | -- | -- |
| `language_and_copy_architecture_v1_3_amendment.md` | `~/Documents/plant-project/05-methodology/current/` | `fef0c3f73e7b06af20591338b38246bfa615ca282ab96714da8c43cd8139bdc3` | 2026-08-20 |

Verify a snapshot against its home:

```sh
shasum -a 256 docs/vendored/language_and_copy_architecture_v1_3_amendment.md \
  ~/Documents/plant-project/05-methodology/current/language_and_copy_architecture_v1_3_amendment.md
```

Two different hashes means the home document moved on and the snapshot is stale. That is
a fact to act on, not a failure -- re-copy and update the row.

## What the current entry carries

`language_and_copy_architecture_v1_3_amendment.md` is the register-pair differentiation
standard: **§9.1** the differentiation test, **§9.2** contradictory pairs, **§9.3**
gloss-avoidance, **§9.4** four schema shapes wearing one suffix, **§9.5** the measured
rate, **§9.5.1** what is still not settled, **§9.6** change log.

**§9.5 holds PLA-256's verdicts**, which exist nowhere else in this repo:
`tools/staging/pla256_round2_batch.md` is the draw and the pre-reading reporting contract,
and its 40 entries carry both register texts with no verdict attached. The rates are here.
