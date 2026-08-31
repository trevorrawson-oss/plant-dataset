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

IF YOU ARE IMPORTING THIS TO WRITE A NEW PROMOTE GUARD SUITE, READ THIS FIRST.
A live fixture buys you nothing if the guards running against it cannot fail. The suite ships
MUTATION-TESTED or it does not ship: one mutation per guard family verified RED, a liveness
defense (MUTATION-APPLIED marker + a sentinel that must redden, else `HARNESS DEAD`), a positive
control where the injection could be invisible, and `assert set(pre) == set(post)` BEFORE any
value comparison -- iterating `pre` makes everything added in `post` invisible, which was all four
PLA-162 defects. A guard that REFUSES an input staying green is a REFUSAL-SPEC pass, not vacuous.
Ruled 2026-08-19 (PLA-215); the bar and its evidence are in
`docs/promote_suite_mutation_convention.md`, the binding line is in CLAUDE.md's Hard rules.
"""
import contextlib
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
    # PLA-6 Round 2: the year-pill trio. The four wave-intermediate SHAs are NOT commits and
    # live in CHAIN; this is the arc's end state, and the only one a fixture can reach by commit.
    '20a32c47f0bf861e5b93fad71b9af3bbb37643afdb70dccd758e1ee0eb080ea9': 'f99f29c',
    '98ea96c446cbeed858efa56bbf5324a7dc2edd3e21bbe26bdaf4c51b90ac6aef': '32a6de9',
    'd04b868c94e45aa7c08dd4de7768040c0462b268f2e9c99eddaf9e6e75beef17': '05de817',
    'd19abe601ab6c67dbf4037f982307ec26a73f921f70334187dc1ed7fd97954f8': '319e388',
    '208e213cb14dce4e2df6b0a48ad49f7e6818337dcd4ce5b1b52691954af542ce': 'f3732cf',
    '75b3c0f0c253ffa7cb420d0f9c9d35e2a04c5dd47d9c222271923b2cc2b41d32': '34c0d26',
    # PLA-8: the iron-phosphate slug-bait safety absolute, 9 fields / 6 crops.
    '6b295d440a8d4bfbad240c0cbf1bfdc83ccad1059c2d615ac8f9f5765e9d69ca': 'cffa4a7',
    # PLA-8 catalog r2: off_season_tillage + certified_clean_stock; prune_out_infection narrowed.
    '6876840ed629ca5a86f4052697426120b2c245d5895c1663e9b8722112f8e670': 'b51bdbc',
    # PLA-8 catalog r3: prompt_harvest, sound_sowing_practice, augmentative_release, resistant_rootstock.
    'afe4d6978aa76ea3a0b8213f8c7f5e57e2dd373292ee20fd14e3f9e04de2fa6e': '0a89792',
    # PLA-8: the Bt safety absolute hedged on nine crops.
    '0f911326d2f4ca20c4b92e199afca3c8e842eb8fa422b1b2a1d537a3d20ac093': '9116050',
    # PLA-8 BATCH 1: 5 crops laddered, roster 7 -> 12.
    '76c7048803a0c68d0924b062a40cfb3d8ffdbaf9a12e316a851f40c9b2255bd4': '9fbf655',
    # PLA-8 catalog r4: exclusion_fencing, closing the vertebrate gap.
    '0754031d02261241e3ef56dda00f165af884101a85a8673db73016a6b2271263': '49d6182',
    # PLA-8 BATCH 2: the four corns, roster 12 -> 16.
    '0e12689ba616bca3316652c9064ca9cbce4aa0c4037b1b69589a1e397abb88a4': 'f389c2d',
    # PLA-8: the Bt safety absolute closed in the catalog method.
    'c13ddea5f1320d766847b707d3795c8cc81251d71ed864f61260f9eeb12e73f5': 'b23e05b',
    'decb944d51e591ef9c7b0f657a258a0a7690f2ad1aa8804dad4b83a235db90c0': '8a02f13',
    '3ec673a76717c0a9fbfe9861d6d63ee36e574d59a88b3e3b3b97cccb29253027': '6671ecd',
    '5696aead08e2e197c06cec78824acf97feac8d8ff67043e82594b4b440b7f71e': 'dda8035',
    'e40cd8ecb612a292880fa4a75f62ebc14267123914fa16d023903c9e63aac9bd': 'cadaa6c',
    'e794969f24a670e5c8573d27a66b6d9d7ad885b8637e1768227a643944d6fe71': '56d33bb',
    # PLA-8 catalog r5: planting_time_avoidance + wet_foliage_discipline; two widenings.
    '48478cb5f62edd284674be3f16a7a08c2537d7d510c19c5e3d89517748c973b1': 'c1e708f',
    # PLA-8: the planting_time_avoidance best_use self-contradiction, closed.
    'acf337809d9085f748bc45b6dfc38dd9c7e88fb92b1408f53879c6bdc0f970a7': '22d176c',
    # PLA-8 BATCH 5: the three beans, roster 24 -> 27.
    '7c3e5d71ae875e013a20b77c3d8dd1f12960bfb8c413e7f8b728df79ef24d145': 'd6e8071',
    # PLA-8 catalog r7: biofungicide + weed_host_control; the planting-time widening refused.
    '4a239eefe1d8627b029dc93e9cc5a990078e377eea0a4c8457dcbafe560002a4': 'febf1af',
    # PLA-8: the powdery-mildew exception on wet_foliage_discipline.
    '17d0eac762fc22b07fb5ec6a83c9f08471202e3c5ddf9bb7010fc861af5f0688': '99a19c6',
    # PLA-8 BATCH 6: the two peas, roster 27 -> 29.
    '3a87737a60c544453497f67bc3744d8534a400cbcba795b6e4b23fdcbabc3cb5': 'd925eb6',
    # PLA-8: mint chlorothalonil, the first chronic-health disclosure.
    '93e32e2b49d9e064b0d687dd5814260186fb71341f072a27b8eec36fa0d578ed': 'd096415',
    # PLA-8: the chlorothalonil backfill, 9 rungs on 6 certified crops.
    '1330fe5d7b1533eaa165b0a48ddad1c8c9ef0335aa3db74f2c545bc447046781': '2e86279',
    '04b5aa69b2f1fd209d84c4affb975cb78df0ee59657f9259b2896edbbe11c5f9': '4afab82',
    # PLA-8: the chemical-cohort close-out; the catalog audit declared closed.
    '674fab251aec7063ffa970f8c81e6156ab6fdbcab1a5800d9a1c93627cdcd740': 'b0c84a1',
    # PLA-8 BATCH 7: the tomatoes; splash_barrier_mulch minted; roster 29 -> 33.
    'f8678adea533447445ee2679d7d333065763a7481c39371b98d0b39d55aeeec1': '2127645',
    # PLA-8 BATCH 8: the leafy greens; fall block opens; roster 33 -> 37.
    '043a7272e76d640f287df420d319f209de8bd4443ffa75d327175958bf3b76e0': 'dd6657a',
    # PLA-8 BATCH 9: the roots; fall block batch 2; roster 37 -> 41.
    '4725bcbbe0cc78046b718c40bb5f97bdcd6638f7f55bec83e1ab465e1a5846f4': '8d395a6',
    # PLA-8 BATCH 10: the brassica family; pyrethrin minted; roster 41 -> 46.
    'be444e25a614e2a8ff95dae7aebaf6835277545e7d4b4e7905f1309355e57234': 'ed0d7b3',
    # PLA-8: mint trap_cropping, the catalog's 59th method. Also reachable via CHAIN (it is the
    # backfill suite's base and was replayed there before this commit existed); _from_commit wins.
    '86c5396a185e34a8b07271dc02794bbd54c7a6dba3367dde832e425c23e0bb2b': '70a2a9e',
    # PLA-8: the trap_cropping backfill, 10 rungs on 9 certified crops.
    '96cbc68c7f8a1509bf922e85ad424d6a55a3f1c2a45d6288bfa5ba16a2bec67a': 'c64f8ed',
    # PLA-8 BATCH 11: alliums + fall herbs; certified_clean_stock widened to nematode; roster
    # 46 -> 50. Also reachable via CHAIN (batch 12 replayed it there before this commit existed);
    # _from_commit is tried first and wins.
    '1e4d0c06ad28ed28642f64a3ae15b537bb7d14367b73280489ebde3befd311ae': '6f2d9d8',
    # PLA-8 BATCH 12: fall finishers; ZERO catalog edits; roster 50 -> 53. Closes the fall block
    # at 20/20. Its base is batch 11's output, which is why that entry sits directly above.
    '7f5079aab0fa4167c87e1373b3d28d598bf2379e05e2f8e2047665eabb13b9c3': '712066c',
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
    # PLA-114 campaign D close. FIVE consecutive PLA-114 states are pinned and all are
    # load-bearing; see the note above. Never amend ae15df4, ebfd537, b7dbc81, 3b222f8 or 8ee1b0b.
    '72284f0291442919d005a8546f6cfbdcdf06502fe7842327fa77201e5c9c8571': '3b222f8',
    # PLA-156 corn dispositions -- one promote, one commit. Its guard suite pins BOTH 72284f02
    # (base) and this (post), so never amend 3b222f8 or 8d00f8a.
    'db853c4b20e889a93d8946e947b31a2c7a00f49042e8774a04dc7386bca9e7a5': '8d00f8a',
    # PLA-156 verification pass -- the two held dispositions corrected. Its suite pins 72284f02,
    # db853c4b AND this, so never amend 3b222f8, 8d00f8a or 8be1ebb.
    'ce9eb12fb85abf9f592ee8bc6621102a5dd785327a74befe2b0e7ddc8146bff5': '8be1ebb',
    # PLA-155 vce_426_331 credit corrections. Its suite pins ce9eb12f AND this, so never
    # amend 503c29f or 8be1ebb.
    '4f6103183ac9c07475b3e0c2d3a71159d0662a10a61383e1d792c049957cac23': '503c29f',
    # PLA-157 zinnia trigger register rotation. Its suite pins 4f610318 AND this, so never
    # amend 596cd65 or 503c29f.
    '060b91b807f7988d3d22ebbae77e90d285ee5f7dfe6a18a11c4de37cf6debbbd': '596cd65',
    'c16071bc34e3f41e0224264adc7d372061ce1b8de9fd2ab61ca5d232b63e4e3b': '46f143e',
    # PLA-202 verbatim rewrite pass. Its suite pins c16071bc (base, replayed to the post
    # state) AND this; never amend 46f143e or e1b3ac3.
    '76f92a20faae0b8e5336ef8e7e1d9c852b9c734c93ae84fc6cccd65f49bcf3ce': 'e1b3ac3',
    '394bb8bdf63c989eeff7241ba41d1c37c829201733ce199f4dffc88490d8f660': '4dde2c8',
    # PLA-253's END state. Its INTERMEDIATE 5f2d9555 is deliberately NOT here -- it was
    # never a commit and lives in CHAIN, rebuilt by replay.
    '3bf8b4ce25fbeaa9f3b2cf7f5b7fe9b5c6344784204780c3f393b2bc2e0eec3e': 'a07bf86',
    # PLA-253 third pass: beneficial_nematodes anchored to pnw_handbook_epn.
    'be8a6d1e10c014906ad66aff03fc307525f6f22d9045ff28cb850ffecfc686f4': '8118eaa',
    # PLA-290: the prose-string variety entries become {id, name, note} records.
    '2d496da51b37c68a60402b82cc30a5252d07e45474b6b98edaf299afbc5c69c4': 'dc5008f',
    # PLA-346: echinacea's paren-variant entry, the last prose variety string.
    'fe26f7833cb9c932fa621c20fb6ebc08af2eb5e66866089e21d847fa4970f57c': 'c2696b4',
    # PLA-8: mint disease_escape_sowing, the catalog's 60th method. Also reachable via CHAIN
    # (it is the backfill suite's base and was replayed there before this commit existed);
    # _from_commit wins.
    '9f38bb007d3abd5b1cfc970178b9a4405088b0a9de46ff27eaba5163bef7b575': 'fd5e7db',
    # PLA-8: the disease_escape_sowing backfill, 7 rungs on 7 certified crops.
    'ee0f54a35a4dd1eee0da6daa5992c636cc422f25796e46d4649fd3c9fcc07277': '7ddac14',
    # PLA-8 BATCH 13: the spring fruiting set (four peppers + eggplant); roster 53 -> 58.
    'b6d366114461fe470aa07c48f18f83ade9e584b86a70898fd12ab5651884088d': '0d45e67',
    # PLA-8: mint mancozeb, the catalog's 61st method. Also reachable via CHAIN (batch 14's
    # base); _from_commit wins.
    '4c5a79d34a435117adee9723242d1846a04045eda739226e6b3419892644c739': 'f9cd212',
    # PLA-8 BATCH 14: okra, tomatillo, and the melons; roster 58 -> 63.
    'c76f14f19f4d2aa208748d0609f14a86bb5753c57fb21840f826e6a9d37599a0': 'b5c75c2',
    # PLA-8 BATCH 15: companions A (the first note-schema batch); roster 63 -> 68.
    '098dd0b18cc85aebf05bbb50071ab9ba1c50bf377afb1235d9359cc07d894bfa': '22dcf6e',
    # PLA-8 BATCH 16: companions B; the Companion & Pollinator category closes; roster 68 -> 73.
    '213cb1108cd4960add0a0f9d3a2bd73aee4f1108d6fa743c6ce6075fd5cc6c2f': '234a088',
    '2a9d3c85dbb2da3ccbd69cd1798017d3ca8a3bb6280b8e212d5f63b86adef4af': 'b196251',
    '2cde361bb3b8571576f94637e65d86f557a44e7807d97b2a94c02eb7c3715198': '9e46e0a',
    # PLA-8 BATCH 18: acid citrus, the first batch on the new ant_exclusion; roster 79 -> 81.
    '514903dbaa59fa66d550fc88525d56dcdfe7150398f6f639e5b5905f1ddf85e4': 'f4355e3',
}

# Uncommitted intermediates from the 2026-07-31 cleanup batch: rebuilt by REPLAY from the
# last committed state, since these promotes ran back-to-back before a commit.


# canonical SHA -> (predecessor SHA, promote script that produces it).
# Hunt 1's intermediate states, which were never committed on their own.
CHAIN = {
    # PLA-6 Round 2 runs the year-pill trio as a PILOT plus rollout WAVES, back to back before
    # a commit, so each wave's base is the previous wave's output and is not a commit. Replay is
    # the only way to rebuild them; each is verified by hash on use, so a wrong link fails loudly.
    '0cc37afe6597d43eac4e867b5eefa625aed5002dfc20628e4a5fbac80215e66b': (
        'fe26f7833cb9c932fa621c20fb6ebc08af2eb5e66866089e21d847fa4970f57c',
        'promote_pla6_year_trio.py'),
    '647fe432076030a3bef240d953a31b04c8a4b31140b445d00b78f1b9a18f108f': (
        '0cc37afe6597d43eac4e867b5eefa625aed5002dfc20628e4a5fbac80215e66b',
        'promote_pla6_wave1.py'),
    '64428067a44b369b550b6d11d8287e7578afbadf022b14e2fe7c8238e0ebc393': (
        '647fe432076030a3bef240d953a31b04c8a4b31140b445d00b78f1b9a18f108f',
        'promote_pla6_wave2.py'),
    '97c63704812e2192fe8ec27ba0007e24db5dadbc88473aeccca5bba217c1521c': (
        '64428067a44b369b550b6d11d8287e7578afbadf022b14e2fe7c8238e0ebc393',
        'promote_pla6_wave3.py'),
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
    # PLA-253 ran two promotes on the same leaf before a commit: the safety rewrite, then
    # the bee hedge as a second pass. 5f2d9555 is the state between them -- a real base
    # for the second suite, and never its own commit, so it is rebuilt by replay.
    '5f2d95559256df1553dd2ac0ba19cfa275ec497ab9ba0264ca28dbd94290af0e': (
        '394bb8bdf63c989eeff7241ba41d1c37c829201733ce199f4dffc88490d8f660',
        'promote_pla253_bt_safety.py'),
    # PLA-8 trap_cropping ships as a mint + backfill pair, the chlorothalonil shape. The mint's
    # output is the backfill suite's base and is not a commit until the mint is committed, so the
    # backfill is verifiable before either lands. Superseded by COMMIT_FOR once the mint commits;
    # _from_commit is tried first, and both paths are hash-verified.
    '86c5396a185e34a8b07271dc02794bbd54c7a6dba3367dde832e425c23e0bb2b': (
        'be444e25a614e2a8ff95dae7aebaf6835277545e7d4b4e7905f1309355e57234',
        'promote_pla8_trap_cropping.py'),
    # PLA-8 disease_escape_sowing ships as a mint + backfill pair, the chlorothalonil /
    # trap_cropping shape. The mint's output is the backfill suite's base and is not a commit
    # until the mint is committed. Superseded by COMMIT_FOR once the mint commits; _from_commit
    # is tried first, and both paths are hash-verified.
    '9f38bb007d3abd5b1cfc970178b9a4405088b0a9de46ff27eaba5163bef7b575': (
        '7f5079aab0fa4167c87e1373b3d28d598bf2379e05e2f8e2047665eabb13b9c3',
        'promote_pla8_disease_escape_sowing.py'),
    # PLA-8 mancozeb mint: batch 14's base is this mint's output (the key must exist in the
    # authoring brief), so it is a CHAIN member until the mint commits. Superseded by COMMIT_FOR
    # once it does; both paths are hash-verified.
    '4c5a79d34a435117adee9723242d1846a04045eda739226e6b3419892644c739': (
        'b6d366114461fe470aa07c48f18f83ade9e584b86a70898fd12ab5651884088d',
        'promote_pla8_mancozeb.py'),
    # PLA-8 batch 12 sits on batch 11's output rather than on live canonical, because parsley
    # REUSES `parsleyworm` -- the id batch 11 mints for dill -- and that string has to exist in
    # the base for the reuse to be a reuse rather than a second, divergent mint of the same
    # problem. Batch 11 is verified but not committed, so its output is reachable only by replay.
    # Superseded by COMMIT_FOR once batch 11 commits; both paths are hash-verified, and if the
    # trap-cropping round lands first this entry goes STALE and fails loud, which is correct.
    '1e4d0c06ad28ed28642f64a3ae15b537bb7d14367b73280489ebde3befd311ae': (
        '96cbc68c7f8a1509bf922e85ad424d6a55a3f1c2a45d6288bfa5ba16a2bec67a',
        'promote_pla8_batch11.py'),
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


def _slug_in(key, crops):
    """The crop slug a table key names, or None if its crop is not in this state.

    Keys come in three shapes -- 'slug', (region, slug), (region, slug, source_id) -- and the
    slug is identified by membership, never by position. Two elements both naming real crops is
    unresolvable and must be an error: guessing would key the presence check to the wrong crop.
    """
    if isinstance(key, str):
        return key if key in crops else None
    matches = [k for k in key if k in crops]
    if len(matches) > 1:
        raise AssertionError('table key %r is ambiguous: %r all name crops in the fixture'
                             % (key, matches))
    return matches[0] if matches else None


@contextlib.contextmanager
def tables_as_of(sha, module, expect_kept):
    """Rebind `module`'s finding-keyed tables to their state AS OF the canonical at `sha`.

    THE PIN PROTECTS THE DATA BUT NOT THE MEASUREMENT (PLA-162): a pinned suite's fixture is
    frozen, but the adjudication tables its analysis module applies are read at run time, so a
    row added for a LATER campaign flips historical assertions red over a fixture that never
    moved. A row whose finding is not on its crop in `pre_state(sha)` simply was not in the
    table at that state, so it is dropped for the duration and restored on exit -- live
    presence tests in the same file must run OUTSIDE this scope and keep seeing the full table.

    `expect_kept` maps table name -> the row count the table held at `sha`. It is REQUIRED and
    load-bearing: the pinned state never changes (pre_state is hash-verified), so the kept
    count is a true constant, stable under live-table growth. Fewer kept means the filter ate a
    row the measurement included; more means a post-pin row escaped it. Without this the helper
    would be its own vacuity generator -- a broken filter emptying a table would turn every
    downstream presence loop into a green no-op.
    """
    import json
    crops = {c['slug']: c for c in json.loads(pre_state(sha))['crops']}
    saved = {}
    try:
        for name, kept in expect_kept.items():
            full = getattr(module, name)
            filtered = {
                k: fid for k, fid in full.items()
                if (lambda slug: slug is not None
                    and module.finding(crops[slug], fid) is not None)(_slug_in(k, crops))
            }
            if len(filtered) != kept:
                raise AssertionError(
                    '%s.%s as of %s: kept %d rows, the pinned measurement expects %d '
                    '(dropped: %s). Fewer than expected means the filter removed a row the '
                    'suite asserts on; more means a post-pin row escaped it.'
                    % (module.__name__, name, sha[:16], len(filtered), kept,
                       sorted(set(full) - set(filtered)) or 'none'))
            saved[name] = full
            setattr(module, name, filtered)
        # the FULL tables, so a live-canonical presence test running inside the scope can
        # still iterate every row -- reading the module attribute there would let post-pin
        # rows escape the live check.
        yield saved
    finally:
        for name, full in saved.items():
            setattr(module, name, full)


@contextlib.contextmanager
def tables_frozen(module, frozen):
    """Rebind RULE-tables to values frozen by hand next to the pinned SHA.

    Rule-tables (IN_SCOPE, RULES, BARE, the hunt rosters) have no keyed record whose presence
    in `pre_state(sha)` could scope them, so fixture-presence filtering cannot protect a suite
    that measures through them -- the value itself must be frozen in the suite, literally,
    beside the SHA it was true at. The saved live value is yielded so the suite's SEPARATE,
    unpinned equality test can assert live == frozen without tautology (inside the scope the
    module attribute IS the frozen value); that one test going red is how a deliberate rule
    change stays loud instead of silently re-baselining a historical measurement.
    """
    saved = {}
    try:
        for name, value in frozen.items():
            if not hasattr(module, name):
                raise AttributeError('%s defines no table %r -- freezing a misspelled name '
                                     'pins nothing while reading as protection'
                                     % (module.__name__, name))
            saved[name] = getattr(module, name)
            setattr(module, name, value)
        yield saved
    finally:
        for name, value in saved.items():
            setattr(module, name, value)


def frozen(module, **values):
    """Pytest fixture factory over `tables_frozen` -- module-scoped, autouse.

        _rules = promote_fixture.frozen(R, HUNTS=HUNTS_AT_PIN, OWN_HUNTS=OWN_HUNTS_AT_PIN)

    A test may request the fixture by name to reach the saved LIVE values for the unpinned
    equality check: `def test_live_hunts_unchanged(_rules): assert _rules['HUNTS'] == ...`.
    """
    import pytest

    @pytest.fixture(autouse=True, scope='module')
    def _rules_frozen():
        with tables_frozen(module, values) as saved:
            yield saved

    return _rules_frozen


def as_of(sha, module, **expect_kept):
    """Pytest fixture factory: assign at module level to pin `module`'s tables for the suite.

        _tables = promote_fixture.as_of(BASE_SHA, R, ANCHOR_FINDING=19, MODELED_FINDING=14)

    Module-scoped and autouse, so every test in the file measures through the pinned tables
    without naming the fixture. Table names are declared, never guessed (opt-in by name), and
    each carries its pinned-state row count -- see `tables_as_of` for why that is load-bearing.
    """
    import pytest

    @pytest.fixture(autouse=True, scope='module')
    def _tables_pinned_as_of():
        with tables_as_of(sha, module, expect_kept) as full:
            yield full

    return _tables_pinned_as_of


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
