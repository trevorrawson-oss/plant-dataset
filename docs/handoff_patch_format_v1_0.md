# Handoff patch format v1.0 (claude.ai -> Claude Code)

**Status:** v1.0, 2026-06-07. The ONE canonical format for a per-session dataset
patch. Applied by `tools/apply_patch.py` (validated against the real M16 5.D / 5e /
6-8 release chain). **claude.ai: emit exactly this; do not invent per-session
variants.** The applier tolerates the historical drifts (see "Tolerated") but new
patches should be canonical.

## The format

```json
{
  "base_sha": "<sha256 of the base crops_data_final.json you authored against>",
  "session": "m16_<crop>_<step>",
  "patches": [
    { "op": "replace", "json_path": "<jsonpath>", "from": <current value>, "value": <new value> },
    { "op": "add",     "json_path": "<jsonpath>",                          "value": <new value> },
    { "op": "delete",  "json_path": "<jsonpath>", "from": <current value> }
  ]
}
```

- **`base_sha` is REQUIRED.** The applier SHA-gates on it and refuses to apply if the
  canonical file has moved. This is what catches "authored against a stale base."
- **`patches`** is the edit list (the applier also accepts `edits` / `patch`).
- One object per leaf change. Order does not matter (each is independently addressed).

## Ops

| op | meaning | guard |
|----|---------|-------|
| `replace` | set an existing leaf to a new value | `from` MUST equal the current value (byte-exact) |
| `add` | populate a slot that is absent or currently `null` | refuses to clobber a present non-null value |
| `delete` | remove a key/element | `from` MUST equal the current value |

`from` is **required** for `replace` and `delete` (it is the drift guard -- if the
base moved under you, the apply fails loudly instead of silently corrupting). For
`add`, omit `from`.

## JSONPath grammar (the only forms supported)

| form | meaning | example |
|------|---------|---------|
| `$` | root | `$.crops...` |
| `name` | dict key (incl. numeric-string keys) | `regions`, `resolved_by_zone.9` |
| `name[N]` | list index | `plantings[0]`, `calendar[6]` |
| `name[?(@.key=='val')]` | first list element whose `key == 'val'` | `crops[?(@.slug=='cherry-tomato')]` |

Any of these may be the final (leaf) token. **Prefer the slug filter over a numeric
crop index** (`crops[?(@.slug=='cherry-tomato')]`, not `crops[0]`) so a reordering of
the crops array cannot mis-target. Inside a region cell, prefer `plantings[?(@.track=='beginner')]`
over `plantings[0]` for the same reason where a stable selector key exists.

Example leaf paths:
- `$.crops[?(@.slug=='cherry-tomato')].watering.amount_beginner`
- `$.crops[?(@.slug=='cherry-tomato')].regions.warm_arid.resolved_by_zone.8.calendar[6]`
- `$.crops[?(@.slug=='cherry-tomato')].regions.ca_desert.plantings[?(@.track=='second_planting')].harvest_start[?(@.label=='fall')].source_quote`

## Tolerated (historical drift the applier normalizes -- do not rely on these)

- Op aliases: `replace_value`->replace, `add_key`->add, `delete_key`/`remove`->delete, `set`->replace.
- Field aliases: `old`/`old_value`->`from`; `new`/`new_value`->`value`; `path`->`json_path`.
- `add` on a present-`null` key (the common mislabel) is accepted (it is really a replace-of-null); `add` on a present non-null value is REFUSED.
- `base_sha` may also be supplied as `_base_sha`.

## Companion: the STATE_HISTORY entry

Every patch is paired with a STATE_HISTORY entry snippet (NOT the whole file).
**If the entry is omitted, Claude Code authors it from the patch** -- but claude.ai
should always provide one. The entry states: start-SHA, what changed (months/dates/
keys), expected gate movement, and the exact path manifest for the claim cross-check.

## Apply (Claude Code)

```
python3 tools/apply_patch.py <patch.json> --base crops_data_final.json --out crops_data_final.scratch.json
```
Then run protocol #6 (whole_crop_gate + release_verify + claim cross-check) before promoting.
