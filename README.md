# plant-dataset/

The single source of truth for `crops_data_final.json` -- the dataset that drives both
vegetables.garden and the future iOS app. Every chat that needs the dataset uploads from
this folder; every session that promotes a new dataset writes back here.

## Folder layout

```
plant-dataset/
├── crops_data_final.json   ← always the current canonical dataset, same filename every time
├── LATEST.txt              ← one line: SHA, date, session name
├── README.md               ← this file
└── archive/                ← every prior promoted version, named with date + session + SHA prefix
    ├── crops_data_final.2026-04-29.mini_integration_3.253e0dbb.json
    └── ...
```

## At chat start

1. Check `LATEST.txt` for the current canonical SHA.
2. Confirm the session's kickoff prompt expects that same SHA. If it does NOT, do not proceed --
   either the kickoff is stale or your dataset is. Reconcile before any work.
3. Upload `crops_data_final.json` (the file at the folder root, not anything in `archive/`).

## At session close (when a session promoted a new dataset)

Claude will produce:
- The new `crops_data_final.json` (in the session's deliverables bundle)
- A copy-paste terminal command for replacing the local files
- A new `LATEST.txt` content line

The terminal command handles four things in order:
1. Verifies the new file's SHA matches the expected value (sanity check).
2. Moves the current `crops_data_final.json` into `archive/` with date + session + SHA-prefix naming.
3. Replaces the top-level `crops_data_final.json` with the new one.
4. Overwrites `LATEST.txt` with the new SHA / date / session.

After running, confirm to Claude that the move happened so the canonical SHA can be recorded
in memory for the next chat to reference.

## SHA verification ritual

The dataset is too large and important to eyeball. Every transition uses SHA-256 to confirm:
- The file Claude promoted in the deliverables bundle is the file you're putting in the folder
- The file you upload at the start of a session is the file the kickoff prompt expects
- The file at session close is the file the new SHA represents

`shasum -a 256 crops_data_final.json` (macOS / Linux) or `Get-FileHash -Algorithm SHA256 crops_data_final.json` (PowerShell) returns the SHA.

`LATEST.txt` is the human-readable cross-check: one line, format

```
<sha256>  <YYYY-MM-DD>  <session_name>
```

Two whitespace-separated columns work the same for human reading and for any future scripted check.

## Archive naming convention

```
crops_data_final.<YYYY-MM-DD>.<session_name>.<SHA8>.json
```

Where `<SHA8>` is the first 8 hex chars of the file's SHA-256. Three benefits:
- Date sort puts versions in chronological order
- Session name says what produced this version
- SHA prefix lets you spot-check any archived version without recomputing the full hash

Example: `crops_data_final.2026-04-29.mini_integration_3.253e0dbb.json`

## What does NOT belong in this folder

- Findings docs, kickoff prompts, corrections inventories, scripts -- those go in their session
  bundles or in project knowledge.
- Fragmentary or in-progress dataset edits -- only promoted, integrity-checked datasets land here.
- Bundles -- the bundle zips can stay wherever you save bundles; only the dataset itself comes here.

## Recovery

If you ever suspect the canonical file has been corrupted or replaced with the wrong version:
1. Compute its SHA (`shasum -a 256 crops_data_final.json`)
2. Compare against `LATEST.txt`
3. If they disagree, the file is wrong, not `LATEST.txt`. Find the matching file in `archive/`
   by SHA-prefix grep:
   ```bash
   ls archive/ | grep "$(head -c 8 LATEST.txt)"
   ```
4. Copy that file back to the top level and re-verify SHA matches `LATEST.txt`.
