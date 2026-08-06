#!/usr/bin/env python3
"""Reconstruct the exact pre-state a promote guard suite was pinned to.

WHY THIS EXISTS. Every promote guard suite in this repo opened with

    if not _is_base():
        print('SKIP: canonical is not the pinned base SHA')
        return

which is correct only while canonical still sits on that promote's base SHA. Canonical moves on
after every promote, so each suite went silently vacuous -- reporting green while running ZERO
checks. Measured 2026-07-30: six suites in that state, and the seventh (cherry-sour) had just
joined them. A promote guard that stops testing without saying so is worse than one that was never
written, because the green is load-bearing in the release gauntlet.

The fix is to stop using live canonical as the fixture and rebuild the pinned pre-state instead.
Two recoveries, in order:

  1. **From a commit.** Most base SHAs are a committed `crops_data_final.json`.
  2. **By replay.** Hunt 1 ran four guarded promotes back to back and committed only the final
     state, so three intermediate base SHAs were never a commit. Each is exactly its predecessor
     plus one promote script, so it is rebuilt by replaying that script. Verified byte-exact.

Every path is HASH-VERIFIED against the requested SHA, so a wrong reconstruction cannot silently
become a fixture. An unresolvable SHA raises -- loudly, never a skip.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, 'tools')

# canonical SHA -> the commit whose crops_data_final.json IS that SHA.
# Verified by hash on every use; a stale entry fails loudly rather than yielding a bad fixture.
COMMIT_FOR = {
    '45409cee243da4196e983198c33505701d44f50842ffb208a224d0b22ddd817b': '7abf386',
    '7ca9e487df51e9d6cd2882c7305c12f536b3733154ac5298bdbd4c0fb079bbe9': 'd8547cd',
    'eb5926edf5e1d75c56ef2f1469bfd1c5cd484c388cb94fc71eb18f9fa8669516': '88a5a21',
    '13d42f95413034636325ff14abb5346d6e044f61ddf313948ff49cdfb82fcda7': '0a4e54f',
    'd5f8307395d681d908857953c13ef51be0e680c6532794a2fb3c6e3aae0925d9': '0015981',
    'd77b9c5166896fa15a815ec25140d9531f966a592abc881fe528875647bb4590': '610dad4',
    'a346915312a1089672c6f333c93e4bc96becaf8a691f8e81db08ee2612e2869e': '57df9e5',
    '72adc3667192a92d086e596cebd935c0ea0ec708cccc0e4611705ffa7f34b5bb': 'baed9d7',
    '1dd6ada3c03477f0d9262b660162c73e83f1ce1539db2c9143bba85f2e99c34c': '8bc30f1',
    '8d2b1a91eea725e66cd6317a4a5a395f0db3b3302fb93e4994262c3e6d42b289': '073d358',
    '172e4e7af950f0b98bf7883f5386c2b701a9d88f4d4347fc30d520cce7e91298': '7092ca1',
    'c6f50a1417a82786356fef764e524641143d41f973dc8f7097eb18454cb3fe5a': '761a128',
    '38a579d4c3e92e470892c9c992215de750f14f5bad02107d6cfc790ebdecc93a': 'c2281f5',
    # campaign A shipped as three commits, so its intermediates are real commits and
    # belong here rather than in CHAIN -- no replay needed to rebuild them.
    'e65aa63ae6154371233edbf076d7f94003652dfbd64980eae3c20a2afb3c76cd': 'afe1ebb',
    '3f6d6ce4430c23ab8b346017be3b9a8963f635fc1178767293d24e2a689eb6f3': '32db451',
    '3b7dc5440ff989e8a3c1d524d3574230f14e50ae0b9c8469edc4b3a93c8271a1': '1fd3ee4',
    # campaign B, the strawberry pass -- its two intermediates are in CHAIN, this is the end state
    '78e5d8e3b649151e4f049aa02cf6de23f05592448942c234e1016802f5652d19': '76db16a',
    # campaign B, the mid_atlantic/ncsu_ext hunt -- one promote, so one commit, no CHAIN entry
    '370806b54252628b49502d3b85476504be24e461bb479445f056d02514f529b7': '4a2f3ec',
    # campaign B closeout (fig, strawberry, apple, elderberry, fava) -- likewise one promote
    '47a502afd95a8248c790ee005e7970672a62434cf4f1cc76dd3e7edac9b62286': '18687d5',
    # campaign B rulings -- Trevor's calls on the 7 open decisions, closing the campaign
    '4065e23bf7cbfd2945c476c93e7326e9a6d2f0646ac88bac9a66f7b9d857023e': 'be3abea',
    # USCRN soil-temp validation (PLA-110) -- one promote, so one commit, no CHAIN entry
    '5a52a76cabb5ca34dcda7756220fcc34db05f408722e27562bdfd96cd4b0b160': 'cad5157',
    # campaign C closeout (PLA-113) -- one promote, so one commit, no CHAIN entry
    '754c51a0de23daceff87c081cd84c6d60274e416fc19639bd2ee2520f5f309f5': '0022763',
    # AZ1005 + divergence + lavender, campaign C's residue -- one promote, one commit
    'ca40d90f008b645a8a01791b30d454759c42d905e1b3fc552ab0c25f9bf07e49': '369321f',
    # PLA-122 rulings on campaign C's five open findings -- one promote, one commit
    '6b2dcb8ed4f51c833fa4d44845b15e7f609079a24a544af025c067dfca45d4db': '8ee1b0b',
    # PLA-114 lemon cold anchor. Pinned by BOTH re-price suites as well as its own promote
    # guards -- test_campaign_c_reprice and test_campaign_d_reprice read `6b2dcb8e` (above)
    # rather than live canonical, so neither this entry nor that one may be rewritten.
    '29b96b65a0969a8ad654762b5d84276bafbd2a8747706cb512ed1414305abf6f': 'ae15df4',
    # PLA-114 task 2, the per-claim credit fix. Its guard suite rebuilds BOTH this entry and
    # `6b2dcb8e`, because the narrowed fourteen-string pin compares the claim text against the
    # state it was originally pinned to, not merely against the previous promote.
    'bce8bcc72aeebb42269b2d96310b427d9502a3670241ca7621e91810588f16cd': 'ebfd537',
    # PLA-114 section 7. Four consecutive PLA-114 states are now pinned, and every one is
    # load-bearing: 6b2dcb8e (both re-price suites + the narrowed fourteen-string pin),
    # 29b96b65 and bce8bcc7 (their own guard suites, re-pointed here from live canonical
    # because this promote legitimately moved past them), and 820af861.
    '820af861e38070a375441803db7e2ddddc72a67e20dd8be580998aa7110a8d1c': 'b7dbc81',
}

# Uncommitted intermediates from the 2026-07-31 cleanup batch: rebuilt by REPLAY from the
# last committed state, since these promotes ran back-to-back before a commit.


# canonical SHA -> (predecessor SHA, promote script that produces it).
# Hunt 1's intermediate states, which were never committed on their own.
CHAIN = {
    'e353fadb83277605192d55fa4312854bf648a835c41666130d41905fc04cc9d2': (
        '172e4e7af950f0b98bf7883f5386c2b701a9d88f4d4347fc30d520cce7e91298',
        'promote_artichoke_findings_key.py'),
    '14c8eab246859c63a3fc9bf68c8f8fcef9ee39f360661589d26245f5924504c3': (
        '13d42f95413034636325ff14abb5346d6e044f61ddf313948ff49cdfb82fcda7',
        'promote_mid_south_uada_citation_findings.py'),
    '5f58654b1fceb057a37cfaec7c77ef5c5d6e3a8de69847781cf237da89121b20': (
        '14c8eab246859c63a3fc9bf68c8f8fcef9ee39f360661589d26245f5924504c3',
        'promote_mid_south_fruit_tree_repoint.py'),
    'd1b441c27f9d1cfe243977e794fc9207ed58361e87ea402af0a37e0845f0f65a': (
        '5f58654b1fceb057a37cfaec7c77ef5c5d6e3a8de69847781cf237da89121b20',
        'promote_mid_south_fruit_corrections.py'),
    # the apple/pawpaw pair shipped in one commit, so the state between them is not a commit
    '8116484c0254efcb4a7de0fc3c398a1404e2b7836db84031e04c0a9d9de4805f': (
        'd5f8307395d681d908857953c13ef51be0e680c6532794a2fb3c6e3aae0925d9',
        'promote_apple_mid_atlantic_bloom_reason.py'),
    # campaign B, the strawberry pass: three promotes run back-to-back before a commit.
    '0ab9b42b58e5a047d302a4dd865b82b997688ad21129a3bd64f2cc1f5116820c': (
        '3b7dc5440ff989e8a3c1d524d3574230f14e50ae0b9c8469edc4b3a93c8271a1',
        'promote_strawberry_mid_south_harvest_repoint.py'),
    '093581673b519fa00337e61a238e99da725eaee7645c2e79d11e2c4f56ba0d51': (
        '0ab9b42b58e5a047d302a4dd865b82b997688ad21129a3bd64f2cc1f5116820c',
        'promote_strawberry_mid_south_z7_anchor.py'),
}

_cache = {}


def _from_commit(sha):
    ref = COMMIT_FOR.get(sha)
    if ref is None:
        return None
    p = subprocess.run(['git', 'show', '%s:crops_data_final.json' % ref],
                       cwd=REPO, capture_output=True)
    return p.stdout if p.returncode == 0 else None


def _from_chain(sha):
    step = CHAIN.get(sha)
    if step is None:
        return None
    parent_sha, script = step
    parent = pre_state(parent_sha)          # recursive; each level hash-verified
    tmp = tempfile.mkdtemp(prefix='fixture_')
    try:
        path = os.path.join(tmp, 'crops.json')
        with open(path, 'wb') as fh:
            fh.write(parent)
        r = subprocess.run([sys.executable, os.path.join(TOOLS, script),
                            '--canonical', path, '--expect-sha', parent_sha, '--apply'],
                           cwd=REPO, capture_output=True, text=True)
        if r.returncode != 0:
            raise AssertionError('replay of %s failed: %s' % (script, (r.stdout + r.stderr)[-400:]))
        with open(path, 'rb') as fh:
            return fh.read()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def pre_state(sha):
    """The exact canonical bytes hashing to `sha`. Raises if it cannot be rebuilt."""
    if sha in _cache:
        return _cache[sha]
    raw = _from_commit(sha) or _from_chain(sha)
    if raw is None:
        raise AssertionError(
            'cannot rebuild the pre-state for %s. Add it to COMMIT_FOR (if it was committed) or '
            'to CHAIN (predecessor SHA + the promote that produces it) in tools/promote_fixture.py. '
            'These guards must FAIL here, never skip.' % sha[:16])
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise AssertionError('rebuilt fixture hashes to %s, expected %s -- history rewritten, or a '
                             'stale COMMIT_FOR/CHAIN entry.' % (got[:16], sha[:16]))
    _cache[sha] = raw
    return raw


def scratch(sha, mutate=None):
    """Write the pre-state to a temp file. `mutate(crops_by_slug, data)` may inject a defect.

    Returns (path, sha_of_written_file).
    """
    import json
    tmp = tempfile.mkdtemp(prefix='promote_fixture_')
    path = os.path.join(tmp, 'crops.json')
    raw = pre_state(sha)
    if mutate is not None:
        data = json.loads(raw)
        mutate({c['slug']: c for c in data['crops']}, data)
        raw = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    with open(path, 'wb') as fh:
        fh.write(raw)
    return path, hashlib.sha256(raw).hexdigest()
