#!/usr/bin/env python3
"""apply_patch.py -- the single canonical applier for claude.ai handoff patches.

Consolidates the per-session resolvers (M16 5.A through 6/7/8) into ONE tool so
Claude Code stops hand-writing a bespoke resolver every release. Reads a patch in
the canonical format, SHA-gates against the base, applies via a JSONPath resolver,
and reports the change footprint (which crops / region cells / top-level keys
moved). It does NOT judge collateral -- that is release_verify's job. This tool
applies + reports; release_verify decides; the operator promotes.

CANONICAL PATCH FORMAT (JSON):
{
  "base_sha": "<sha256 of the base crops_data_final.json>",   # REQUIRED -- gated
  "patches": [                                                 # alias: "edits" | "patch" | "ops"
    {"op": "replace", "json_path": "<jsonpath>", "from": <current>, "value": <new>},
    {"op": "add",     "json_path": "<jsonpath>",                      "value": <new>},
    {"op": "delete",  "json_path": "<jsonpath>", "from": <current>}
  ]
}
Edit-field aliases accepted (claude.ai has drifted on these): from|old|old_value ;
value|new|new_value ; json_path|path .

OPS (each is from-guarded for safety -- the guard, not the label, is authoritative,
so the common add-vs-replace mislabel cannot corrupt data):
  replace -- assert current == `from`, then set `value`.
  add     -- target must be ABSENT or empty-equivalent (null / [] / {} / ""); then set
             `value`. (Tolerates the frequent "add" label on an unpopulated wipe slot,
             however the wipe typed its emptiness; refuses to clobber a present,
             NON-empty value.)
  delete  -- assert current == `from`, then remove the key/element.

JSONPATH GRAMMAR (bracket-aware; the filter's inner `.` does not split tokens):
  $                          root
  name                       dict key (incl. numeric-string keys, e.g. resolved_by_zone.9)
  name[N]                    list index
  name[?(@.key=='val')]      list filter -- first element whose [key] == 'val'
  ...any of the above may be the final (leaf) token.

USAGE:
  python3 tools/apply_patch.py <patch.json> [--base crops_data_final.json]
          [--out crops_data_final.scratch.json] [--quiet]
  --base defaults to ./crops_data_final.json ; --out defaults to <base>.scratch.json
Exit 1 on: SHA mismatch, unresolved path, a from-guard failure, or an add onto a
present non-null value.
"""
import json, hashlib, sys, re, argparse

FILT = re.compile(r"^([^\[]+)\[\?\(@\.([^=]+)==\'([^\']+)\'\)\]$")
IDX = re.compile(r"^([^\[]+)\[(\d+)\]$")
BSLUG = re.compile(r"^([^\[]+)\[([^\]?=]+)\]$")  # name[token]; non-numeric token -> slug/id lookup
_MISSING = object()


def normalize_path(path, slug):
    """Normalize the path forms claude.ai actually emits to a crop-rooted path:
      - canonical `$.crops[?(@.slug=='X')]...`           -> unchanged
      - bracket-slug `crops[X].regions...` (Step 4)       -> unchanged (BSLUG resolves it)
      - $-rooted crop-relative `$.pests[0]...` (steps678) -> prefix the crop filter
      - bare crop-relative `regions.warm_arid...`         -> prefix the crop filter
      - JSON-Pointer crop-relative `/sunlight`, `/soil/x`, `/opts/0/name` (peach S1-3) -> a.b / a[0].b
    Crop-relative prefixing requires a known target slug (from the envelope/--slug)."""
    p = path.strip()
    # RFC-6901 JSON-Pointer form (claude.ai peach Steps 1-3 drift): leading '/', '/'-separated.
    # Convert to the dot/bracket crop-relative form the rest of this function expects.
    if p.startswith("/"):
        rebuilt = ""
        for seg in p.split("/")[1:]:
            seg = seg.replace("~1", "/").replace("~0", "~")  # pointer unescape
            if seg.lstrip("-").isdigit():
                rebuilt += f"[{seg}]"
            else:
                rebuilt += ("." + seg) if rebuilt else seg
        p = rebuilt
    if p.startswith("$."):
        p = p[2:]
    elif p == "$":
        return path
    elif p.startswith("$"):
        p = p[1:]
    first = p.split(".", 1)[0].split("[", 1)[0]
    if first == "crops":
        return "$." + p
    if slug:
        return f"$.crops[?(@.slug=='{slug}')]." + p
    return "$." + p   # no slug known: leave crop-relative (will fail loudly at resolve)


def tokenize(path):
    """Split a JSONPath on '.' but never inside [...] (the filter has an inner '.')."""
    toks, cur, depth = [], "", 0
    for ch in path:
        if ch == "[":
            depth += 1; cur += ch
        elif ch == "]":
            depth -= 1; cur += ch
        elif ch == "." and depth == 0:
            if cur:
                toks.append(cur); cur = ""
        else:
            cur += ch
    if cur:
        toks.append(cur)
    return [t for t in toks if t != "$"]


def _parse(tok):
    m = FILT.match(tok)
    if m:
        return ("filter", m.group(1), (m.group(2), m.group(3)))
    m = IDX.match(tok)
    if m:
        return ("index", m.group(1), int(m.group(2)))
    m = BSLUG.match(tok)
    if m and not m.group(2).isdigit():
        return ("slugfilter", m.group(1), m.group(2))
    return ("key", tok, None)


def _child(node, tok):
    kind, key, sel = _parse(tok)
    if kind == "filter":
        for el in node[key]:
            if str(el.get(sel[0])) == sel[1]:
                return el
        raise KeyError(f"filter matched nothing: {tok}")
    if kind == "slugfilter":
        for el in node[key]:
            if isinstance(el, dict) and any(str(el.get(idk)) == sel
                                            for idk in ("slug", "id", "region_id", "track")):
                return el
        raise KeyError(f"slug/id filter matched nothing: {tok}")
    if kind == "index":
        child = node[key]
        # RFC-6901: a numeric token against a DICT is a string key, not a list index
        # (e.g. resolved_by_zone is keyed by zone-string "3".."11"). Against a list it
        # stays an index (rootstock_options[0]). Branch on the actual node type.
        return child[str(sel)] if isinstance(child, dict) else child[sel]
    return node[key]


def resolve_parent(root, path):
    """Return (parent_container, leaf_token). Raises KeyError/IndexError if a non-leaf step misses."""
    toks = tokenize(path)
    node = root
    for t in toks[:-1]:
        node = _child(node, t)
    return node, toks[-1]


def leaf_get(container, leaf):
    """Current value at the leaf, or _MISSING if the slot is absent."""
    kind, key, sel = _parse(leaf)
    if kind in ("filter", "slugfilter"):
        try:
            return _child(container, leaf)
        except KeyError:
            return _MISSING
    if kind == "index":
        child = container.get(key) if isinstance(container, dict) else None
        if isinstance(child, dict):            # numeric token vs a dict -> string key
            return child.get(str(sel), _MISSING)
        if not isinstance(child, list) or not (0 <= sel < len(child)):
            return _MISSING
        return child[sel]
    if isinstance(container, dict):
        return container.get(key, _MISSING)
    return _MISSING


def leaf_set(container, leaf, value):
    kind, key, sel = _parse(leaf)
    if kind == "index":
        child = container[key]
        if isinstance(child, dict):          # numeric token vs a dict -> string key
            child[str(sel)] = value
        elif sel == len(child):
            child.append(value)              # index == len -> APPEND a new entry
        elif 0 <= sel < len(child):
            child[sel] = value
        else:
            raise IndexError(f"index {sel} out of range (len {len(child)}) for leaf {leaf!r}")
    elif kind in ("filter", "slugfilter"):
        raise ValueError(f"cannot set a filter as a leaf: {leaf}")
    else:
        container[key] = value


def leaf_del(container, leaf):
    kind, key, sel = _parse(leaf)
    if kind == "index":
        child = container[key]
        del child[str(sel) if isinstance(child, dict) else sel]
    elif kind in ("filter", "slugfilter"):
        raise ValueError(f"cannot delete a filter leaf: {leaf}")
    else:
        del container[key]


def _get(edit, *names):
    for n in names:
        if n in edit:
            return edit[n]
    return _MISSING


def _is_empty(x):
    """Empty-equivalent: the wipe AND the schema-2.9 migration type unpopulated slots
    inconsistently -- null / [] / {} / '' scalars, and 2.9 scaffolds the universal blocks
    (watering/fertilizer/soil/ph/container_notes/...) as null-KEYED dicts (not {}). So a
    dict/list whose every leaf is itself empty-equivalent is empty (recursive). A container
    carrying ANY real (non-empty) leaf is NOT empty -- the clobber guard stays intact."""
    if x is None or x == [] or x == {} or x == "":
        return True
    if isinstance(x, dict):
        return all(_is_empty(v) for v in x.values())
    if isinstance(x, list):
        return all(_is_empty(v) for v in x)
    return False


# claude.ai has emitted several op vocabularies across sessions; normalize to canonical.
OP_ALIASES = {
    "replace": "replace", "replace_value": "replace", "set": "replace", "set_value": "replace",
    "add": "add", "add_key": "add",
    "delete": "delete", "delete_key": "delete", "remove": "delete",
}


def normalize_envelope(patch):
    """Return (base_sha, edits, target_slug) from EITHER the canonical format
    {base_sha, patches:[...]} OR the grouped {_meta, corrections:[{...,changes:[...]}]}
    wrapper claude.ai emitted for beefsteak Step 4. Flattens corrections[*].changes[*]."""
    meta = patch.get("_meta") or {}
    base_sha = (patch.get("base_sha") or patch.get("_base_sha")
                or meta.get("base_sha") or meta.get("start_sha"))
    slug = (meta.get("target_crop_slug") or meta.get("crop_slug")
            or meta.get("target_crop") or meta.get("crop")
            or patch.get("crop_slug") or patch.get("target_crop")
            or patch.get("crop"))   # top-level `crop` (peach Steps 1-3 envelope)
    edits = patch.get("patches", patch.get("edits", patch.get("patch", patch.get("ops"))))
    if edits is None and "corrections" in patch:
        edits = []
        for corr in patch["corrections"]:
            edits.extend(corr.get("changes") or corr.get("edits") or [])
    return base_sha, edits, slug


def apply_patch(data, patch, slug=None):
    base_sha, edits, env_slug = normalize_envelope(patch)
    slug = slug or env_slug
    if edits is None:
        sys.exit("patch has no 'patches'/'edits'/'patch'/'corrections' list")
    for i, e in enumerate(edits):
        raw_op = e["op"]
        op = OP_ALIASES.get(raw_op)
        if op is None:
            sys.exit(f"edit {i}: unknown op {raw_op!r} (known: {sorted(set(OP_ALIASES))})")
        path = _get(e, "json_path", "path")
        if path is _MISSING:
            sys.exit(f"edit {i}: no json_path/path")
        path = normalize_path(path, slug)
        try:
            parent, leaf = resolve_parent(data, path)
        except (KeyError, IndexError, TypeError) as ex:
            sys.exit(f"edit {i}: unresolved path {path} ({ex})")
        cur = leaf_get(parent, leaf)
        frm = _get(e, "from", "old", "old_value")
        val = _get(e, "value", "new", "new_value", "after")
        before = _get(e, "before")
        if op == "replace":
            # The wipe types empties inconsistently (lists [], dicts {}, scalars null); claude.ai
            # often guards with `from:null`. An empty-vs-empty mismatch is NOT drift -- the slot
            # was unpopulated as claimed. A POPULATED cur vs the guard still halts (base_sha is the
            # authoritative drift gate; this guard only catches overwriting real content).
            if (frm is not _MISSING and cur != frm
                    and not (_is_empty(cur) and _is_empty(frm))
                    and not (val is not _MISSING and cur == val)):
                sys.exit(f"edit {i} FROM-GUARD: {path}\n  have: {json.dumps(cur, ensure_ascii=False)[:160]}\n  want: {json.dumps(frm, ensure_ascii=False)[:160]}")
            # The grouped `corrections` format supplies a PROSE `before` summary, not a
            # byte-exact guard. When no real `from` is given, the patch-level base_sha
            # gate is the drift protection; surface a note for operator visibility.
            if frm is _MISSING and before is not _MISSING and cur != before:
                print(f"  note: edit {i} 'before' is advisory (not byte-equal to current); relying on base_sha gate -- {path}")
            leaf_set(parent, leaf, val)
        elif op == "add":
            # The wipe types unpopulated slots as null / [] / {} / "" inconsistently, and
            # claude.ai emits `add` for them. Tolerate an empty-equivalent cur (mirrors the
            # replace path's _is_empty drift-absorption); a POPULATED cur still halts so a
            # real clobber is caught. (An absent slot / append-at-len index is _MISSING.)
            if cur is not _MISSING and not _is_empty(cur):
                sys.exit(f"edit {i} ADD onto present non-null value (refusing to clobber): {path}\n  have: {json.dumps(cur, ensure_ascii=False)[:160]}")
            leaf_set(parent, leaf, val)
        elif op == "delete":
            if cur is _MISSING:
                sys.exit(f"edit {i} DELETE but slot absent: {path}")
            if frm is not _MISSING and cur != frm:
                sys.exit(f"edit {i} DELETE FROM-GUARD: {path}\n  have: {json.dumps(cur, ensure_ascii=False)[:160]}\n  want: {json.dumps(frm, ensure_ascii=False)[:160]}")
            leaf_del(parent, leaf)
        else:
            sys.exit(f"edit {i}: unknown op {op!r}")
    return len(edits)


def footprint(before, after):
    """Report what moved -- crops, region cells, top-level non-crop keys, catalog delta."""
    out = []
    bc = {c["slug"]: c for c in before["crops"]}
    ac = {c["slug"]: c for c in after["crops"]}
    changed_crops = sorted(s for s in ac if ac[s] != bc.get(s))
    out.append(f"crops changed: {changed_crops or 'none'}")
    tl = sorted(k for k in after if k != "crops" and after.get(k) != before.get(k))
    out.append(f"top-level (non-crops) changed: {tl or 'none'}")
    if "source_catalog" in after and "source_catalog" in before:
        add = sorted(set(after["source_catalog"]) - set(before["source_catalog"]))
        rm = sorted(set(before["source_catalog"]) - set(after["source_catalog"]))
        out.append(f"catalog +{add or 'none'} -{rm or 'none'}")
    for s in changed_crops:
        ar = ac[s].get("regions") or {}
        br = bc.get(s, {}).get("regions") or {}
        cells = sorted(r for r in ar if ar[r] != br.get(r))
        if cells:
            out.append(f"  {s} region cells changed: {cells}")
    return out


def verify_proposed_sha(text, proposed):
    """claude.ai sometimes computes its proposed end-SHA with ensure_ascii=True
    (degF -> the 6-char \\u00b0F escape); canonical is ensure_ascii=False. Try BOTH
    and report which matched, so the operator isn't left guessing."""
    canon = hashlib.sha256(text.encode()).hexdigest()
    ascii_text = json.dumps(json.loads(text), separators=(",", ":"), ensure_ascii=True)
    ascii_sha = hashlib.sha256(ascii_text.encode("utf-8")).hexdigest()
    if proposed == canon:
        return "proposed end-SHA matches CANONICAL (ensure_ascii=False) -- correct"
    if proposed == ascii_sha:
        return f"proposed end-SHA matches ASCII-ESCAPED (ensure_ascii=True) -- claude.ai used the wrong encoding; canonical is {canon}"
    return f"proposed end-SHA MATCHES NEITHER encoding; canonical={canon} ascii={ascii_sha}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patch")
    ap.add_argument("--base", default="crops_data_final.json")
    ap.add_argument("--out", default=None)
    ap.add_argument("--slug", default=None, help="target crop slug for crop-relative paths (overrides envelope)")
    ap.add_argument("--validate", action="store_true", help="dry-run: resolve paths + report footprint, write nothing")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    out = a.out or (a.base.rsplit(".json", 1)[0] + ".scratch.json")

    raw = open(a.base, "rb").read()
    actual = hashlib.sha256(raw).hexdigest()
    patch = json.load(open(a.patch))
    base_sha, _edits, env_slug = normalize_envelope(patch)
    slug = a.slug or env_slug
    if not base_sha:
        sys.exit("patch has no base_sha / _meta.start_sha -- refusing to apply unanchored")
    if actual != base_sha:
        sys.exit(f"SHA mismatch: base file is {actual}\n              patch expects {base_sha}\n  STOP -- re-preflight.")

    import copy as _copy
    data = json.loads(raw)
    before = _copy.deepcopy(data)
    n = apply_patch(data, patch, slug=slug)
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    new_sha = hashlib.sha256(text.encode()).hexdigest()

    if not a.quiet:
        print(f"{'VALIDATED' if a.validate else 'applied'} {n} edits; base {base_sha[:8]} -> out {new_sha[:8]}")
        for line in footprint(before, data):
            print("  " + line)
        print(f"  escaped-unicode in output: {text.count(chr(92) + 'u')} (want 0)")
        proposed = (patch.get('_meta') or {}).get('end_sha') or patch.get('end_sha') or patch.get('proposed_sha')
        if proposed:
            print("  " + verify_proposed_sha(text, proposed))
    if a.validate:
        print(f"OUT_SHA={new_sha}  (validate-only; nothing written)")
        return
    open(out, "w").write(text)
    if not a.quiet:
        print(f"  wrote {out}")
    print(f"OUT_SHA={new_sha}")


if __name__ == "__main__":
    main()
