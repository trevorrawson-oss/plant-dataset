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
  "patches": [                                                 # alias: "edits" | "patch"
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
  add     -- target must be ABSENT or present-as-null; then set `value`. (Tolerates
             the frequent "add" label on a present-null key; refuses to clobber a
             present NON-null value.)
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
_MISSING = object()


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
    return ("key", tok, None)


def _child(node, tok):
    kind, key, sel = _parse(tok)
    if kind == "filter":
        for el in node[key]:
            if str(el.get(sel[0])) == sel[1]:
                return el
        raise KeyError(f"filter matched nothing: {tok}")
    if kind == "index":
        return node[key][sel]
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
    if kind == "filter":
        try:
            return _child(container, leaf)
        except KeyError:
            return _MISSING
    if kind == "index":
        lst = container.get(key) if isinstance(container, dict) else None
        if not isinstance(lst, list) or not (0 <= sel < len(lst)):
            return _MISSING
        return lst[sel]
    if isinstance(container, dict):
        return container.get(key, _MISSING)
    return _MISSING


def leaf_set(container, leaf, value):
    kind, key, sel = _parse(leaf)
    if kind == "index":
        container[key][sel] = value
    elif kind == "filter":
        raise ValueError(f"cannot set a filter as a leaf: {leaf}")
    else:
        container[key] = value


def leaf_del(container, leaf):
    kind, key, sel = _parse(leaf)
    if kind == "index":
        del container[key][sel]
    elif kind == "filter":
        raise ValueError(f"cannot delete a filter leaf: {leaf}")
    else:
        del container[key]


def _get(edit, *names):
    for n in names:
        if n in edit:
            return edit[n]
    return _MISSING


# claude.ai has emitted three op vocabularies across sessions; normalize to canonical.
OP_ALIASES = {
    "replace": "replace", "replace_value": "replace", "set": "replace",
    "add": "add", "add_key": "add",
    "delete": "delete", "delete_key": "delete", "remove": "delete",
}


def apply_patch(data, patch):
    edits = patch.get("patches", patch.get("edits", patch.get("patch")))
    if edits is None:
        sys.exit("patch has no 'patches'/'edits'/'patch' list")
    for i, e in enumerate(edits):
        raw_op = e["op"]
        op = OP_ALIASES.get(raw_op)
        if op is None:
            sys.exit(f"edit {i}: unknown op {raw_op!r} (known: {sorted(set(OP_ALIASES))})")
        path = _get(e, "json_path", "path")
        if path is _MISSING:
            sys.exit(f"edit {i}: no json_path/path")
        try:
            parent, leaf = resolve_parent(data, path)
        except (KeyError, IndexError, TypeError) as ex:
            sys.exit(f"edit {i}: unresolved path {path} ({ex})")
        cur = leaf_get(parent, leaf)
        frm = _get(e, "from", "old", "old_value")
        val = _get(e, "value", "new", "new_value")
        if op == "replace":
            if frm is not _MISSING and cur != frm:
                sys.exit(f"edit {i} FROM-GUARD: {path}\n  have: {json.dumps(cur, ensure_ascii=False)[:160]}\n  want: {json.dumps(frm, ensure_ascii=False)[:160]}")
            leaf_set(parent, leaf, val)
        elif op == "add":
            if cur is not _MISSING and cur is not None:
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patch")
    ap.add_argument("--base", default="crops_data_final.json")
    ap.add_argument("--out", default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    out = a.out or (a.base.rsplit(".json", 1)[0] + ".scratch.json")

    raw = open(a.base, "rb").read()
    actual = hashlib.sha256(raw).hexdigest()
    patch = json.load(open(a.patch))
    base_sha = patch.get("base_sha") or patch.get("_base_sha")
    if not base_sha:
        sys.exit("patch has no base_sha -- refusing to apply unanchored")
    if actual != base_sha:
        sys.exit(f"SHA mismatch: base file is {actual}\n              patch expects {base_sha}\n  STOP -- re-preflight.")

    import copy as _copy
    data = json.loads(raw)
    before = _copy.deepcopy(data)
    n = apply_patch(data, patch)
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    open(out, "w").write(text)
    new_sha = hashlib.sha256(text.encode()).hexdigest()
    if not a.quiet:
        print(f"applied {n} edits; base {base_sha[:8]} -> out {new_sha[:8]}")
        for line in footprint(before, data):
            print("  " + line)
        print(f"  escaped-unicode in output: {text.count(chr(92) + 'u')} (want 0)")
        print(f"  wrote {out}")
    print(f"OUT_SHA={new_sha}")


if __name__ == "__main__":
    main()
