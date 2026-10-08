"""live_pin_registry -- every test in tools/ pinned to the LIVE canonical (housekeeping kickoff 60, ruling 3, 2026-10-03).

A LIVE PIN asserts, against the live canonical (read directly, a scratch copy of it, or gate_all / whole_crop_gate /
release_verify run on it), a value a legitimate promote can move: the canonical's SHA, or a population (a count, an
identity set, a roster), as an equality or a floor. PLA-544 found these one failure at a time (the collision gate's
PINNED_SHA went stale at ab44218; bare_host_scan's population rode four promotes), and its 2026-09-30 inventory was
named, not measured: it missed test_gate_planting_layout_a44's gate_all line. This registry is the measured list.

THE RULE (ruled 2026-10-03). A pin's SHA label means "last moved at" and is never edited on a re-verify. Every
promote's DATA commit message records "re-verified at <sha>" for every entry in LIVE_PINS (print the list with
`python3 tools/live_pin_registry.py`); a pin that went red is re-measured with its rows read, never retuned blind.

COMPLETENESS (test_live_pin_registry.py): detect() flags every tools/test_*.py that reads the live canonical AND
carries a known canonical-SHA literal, an integer literal >= 10 in an equality or a floor, or an asserted string with a
2+-digit number beside a population noun. Every flagged file must be in LIVE_PINS or EXEMPT (with its reason), so a
new pin cannot ride unregistered. The positive control is A44's omission. LIVE_PINS also carries live pins the
detector cannot see, each saying why (a helper-loaded canonical, a floor under 10, a ruled addition).
Content pins (values on named live cells) are recorded where they sit in a live-pin file; a file whose only live
dependency is content is EXEMPT as CONTENT, per the ruling's definition (SHA or population).
Measured 2026-10-03/04 on b331e5f2: 62 detected files (61 + this registry's own test); 60 after B5 turned
test_build_rgv_promote into a replay and test_rgv_harness into an injection (both stay EXEMPT, reasons updated), every one read and classified (kickoff 60 B6).
"""
import ast, glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

LIVE = re.compile(r"crops_data_final\.json|\bCANON\b|gate_all|whole_crop_gate|release_verify")
POPSTR = re.compile(r"\b\d{2,}(?:,\d{3})*\s+(?:certified|crops?|entries|entry|rows?|anchors?|citations?|blocks?|cells?|"
                    r"leaves|leaf|nodes?|sole|decisions?|perennials?|annuals?|shells?|launch|records?|figures?)\b|"
                    r"inspected\s+\d{2,}", re.I)


def canonical_prefixes():
    """8-hex prefixes of every canonical SHA the repo has named: promote_fixture's pins and LATEST.txt's history."""
    known = set(re.findall(r"['\"]([0-9a-f]{64})['\"]", open(os.path.join(HERE, "promote_fixture.py")).read()))
    log = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "--", "LATEST.txt"], capture_output=True,
                         text=True).stdout.split()
    for h in log:
        txt = subprocess.run(["git", "-C", REPO, "show", f"{h}:LATEST.txt"], capture_output=True, text=True).stdout
        known |= set(re.findall(r"\b([0-9a-f]{64})\b", txt))
    return {k[:8] for k in known}


def _int_lit(c):
    return isinstance(c, ast.Constant) and type(c.value) is int and c.value >= 10


def _has_int(c):
    return _int_lit(c) or (isinstance(c, ast.Tuple) and any(_int_lit(e) for e in c.elts))


def arms(src, prefixes):
    """(canonical-SHA prefixes, int equalities, int floors, population strings) found in one test file's source."""
    tree = ast.parse(src)
    sha = sorted({x[:8] for x in re.findall(r"\b[0-9a-f]{8,64}\b", src) if x[:8] in prefixes})
    eq = fl = ps = 0
    for x in ast.walk(tree):
        if isinstance(x, ast.Compare) and any(_has_int(c) for c in [x.left] + x.comparators):
            if any(isinstance(o, ast.Eq) for o in x.ops):
                eq += 1
            if any(isinstance(o, (ast.GtE, ast.Gt, ast.LtE, ast.Lt)) for o in x.ops):
                fl += 1
        if isinstance(x, ast.Call) and getattr(x.func, "attr", "") in (
                "assertEqual", "assertGreaterEqual", "assertGreater", "assertLessEqual"):
            if any(_has_int(c) for c in x.args):
                if x.func.attr == "assertEqual":
                    eq += 1
                else:
                    fl += 1
        if isinstance(x, (ast.Assert, ast.Call)):
            for c in ast.walk(x):
                if isinstance(c, ast.Constant) and isinstance(c.value, str) and POPSTR.search(c.value):
                    ps += 1
    return sha, eq, fl, ps


def detect(tools_dir=HERE, prefixes=None):
    """{file name: arms} for every tools/test_*.py that reads the live canonical and carries a pin-shaped literal."""
    prefixes = canonical_prefixes() if prefixes is None else prefixes
    out = {}
    for p in sorted(glob.glob(os.path.join(tools_dir, "test_*.py"))):
        src = open(p, encoding="utf-8", errors="replace").read()
        if not LIVE.search(src):
            continue
        try:
            a = arms(src, prefixes)
        except SyntaxError:
            continue
        if a[0] or a[1] or a[2] or a[3]:
            out[os.path.basename(p)] = a
    return out


# file -> [(test, kind equality|floor|ceiling, class sha|population|content, what it asserts, line)]
LIVE_PINS = {
    # PLA-673 (2026-10-05): the glossary sense guard reads the LIVE canonical's hill-word consumer leaves. A promote that
    # adds or rewords a hill / hills / hilled / hilling leaf moves these (re-measure with the leaves read). MOVED at
    # PLA-673 part B2 (aaf004a2): 232 -> 225; MOVED at part D (5420479d, 2026-10-06): 225 -> 224, hill 102 -> 103, none
    # 63 -> 61 (both peppers' prevention leaves lose their hill-word; watermelon thinning.method gains one). Part D adds
    # the D8 empty-population pin and the shared fixture's case count / sole-case map (read against the live glossary).
    'test_glossary_sense.py': [
        ('test_glossary_sense.py::test_population_is_224_consumer_leaves', 'equality', 'population', 'LIVE.inspected == 224; len(LIVE.rows) == 224', 49),
        ('test_glossary_sense.py::test_the_default_call_accepts_the_live_roster', 'equality', 'population', 'classify_dataset(DATA, SPEC).inspected == 224', 66),
        ('test_glossary_sense.py::test_live_term_counts', 'equality', 'population', 'by == {hill: 103, hilling: 60, none: 61}', 77),
        ('test_glossary_sense.py::test_injected_non_consumer_leaf_is_not_inspected', 'equality', 'population', 'inspected == 224 after an injection', 108),
        ('test_glossary_sense.py::test_potato_all_44_live_leaves_are_hilling', 'equality', 'population', 'len(potato rows) == 44', 163),
        ('test_glossary_sense.py::test_strawberry_hill_system_live_leaves_are_none', 'equality', 'population', 'len(strawberry rows) == 7', 205),
        ('test_glossary_sense.py::test_name_exclusions_live', 'equality', 'population', 'per-exclusion live leaf counts (NAMES table: Hill Hardy 31, Madalene 1, Hill Country 7, Beverly Hills 2, Mediterranean 2, Hawaii 11)', 250),
        ('test_glossary_sense.py::test_glossary_entries_with_the_seven_keys_load', 'equality', 'population', 'classify_dataset(DATA, spec).inspected == 224', 318),
        ('test_glossary_sense.py::test_d8_no_pepper_or_eggplant_leaf_carries_a_hill_word_after_part_d', 'equality', 'population', 'pepper / eggplant hill-word leaves == [] (D8 exclusion matches no live leaf)', 128),
        ('test_glossary_sense.py::test_every_refuse_on_pattern_is_exercised_alone_or_waived', 'equality', 'content', 'each refuse_on pattern of the LIVE glossary drives exactly its SOLE_CASE fixture case (2 waived UNREACHABLE)', 396),
    ],
    'test_annual_calendar.py': [
        ('module-level', 'equality', 'population', '_got == _PINNED_ANNUALS (84 slugs by identity)', 266),
        ('module-level', 'floor', 'population', 'len(_annuals) >= 10', 243),
    ],
    'test_bare_host_gate.py': [
        ('test_bare_host_gate.py::LiveCanonical::test_population_and_verdict', 'equality', 'population', 'set(sole) == set(G.KNOWN) (381 waived SOLE identities)', 89),
        ('test_bare_host_gate.py::LiveCanonical::test_population_and_verdict', 'floor', 'population', 'insp >= G.MIN_INSPECTED (28000, pinned at :75)', 87),
        ('test_bare_host_gate.py::PinsAreTheMeasurement::test_waiver_file_is_the_measured_population', 'equality', 'sha', "_KNOWN_DOC['measured_on'] == SHA (00dda31c..); count == 381", 70),
        ('test_bare_host_gate.py::LiveCanonical::test_the_named_examples', 'equality', 'content', "Flying Dragon rows SOLE; lemon TAMU rows co-cited; grapefruit/orange-navel rootstock_options[2] sources == ['ucr_citrus'] at UCR url", 96),
        ('test_bare_host_gate.py::LiveCanonical::test_the_self_pathed_blind_spot_is_real_and_closed', 'equality', 'content', "('grapefruit','rootstock_options[2]','ucr_citrus') in self_pathed; orange-navel not", 107),
    ],
    'test_bare_host_scan.py': [
        ('test_bare_host_scan.py::test_self_pathed_population_at_this_canonical', 'ceiling (red on growth)', 'population', 'live self-pathed rows - known == {} (321 identities in bare_host_self_pathed_known.json)', 131),
        ('test_bare_host_scan.py::test_self_pathed_sole_split_is_pinned_by_identity', 'equality', 'population', 'SOLE status of every present pinned row == sole_identities (161)', 145),
        ('test_bare_host_scan.py::test_lemon_already_resolves_clemson_hgic_to_one_document', 'equality', 'population', "len(pathed['clemson_hgic']) == 14; urls == {CLEMSON_COLD}", 80),
        ('test_bare_host_scan.py::test_self_pathed_pin_is_the_measured_population', 'equality', 'sha', "measured_on.startswith('00dda31c'); count == 321; decisions == 80; crops == 37", 118),
        ('test_bare_host_scan.py::test_the_hunt_28_node_is_still_bare_and_still_masked', 'equality', 'content', "exactly one bare row for HUNT_28, url == 'https://hgic.clemson.edu', is_sole False", 67),
    ],
    'test_calendar_basis_gate.py': [
        ('module-level', 'floor', 'population', 'len(cert) >= 18', 63),
    ],
    'test_campaign_c_reprice.py': [
        ('live findings', 'floor', 'population', 'n > 300 and chars > 80_000 on live findings; live content checks (ruled onto the list, kickoff 60 ruling 3)', 434),
    ],
    'test_campaign_d_reprice.py': [
        ('live findings', 'equality', 'content', 'live content checks :425/:440/:445 (ruled onto the list, kickoff 60 ruling 3)', 425),
    ],
    'test_catalog_divergence_scan.py': [
        ('module-level', 'floor', 'population', 'two live population floors > 500 (detector miss: canonical loaded through a helper)', 91),
    ],
    'test_doc_roster_claim_gate.py': [
        ('module-level', 'equality', 'population', "REAL['total'] == 128", 148),
        ('module-level', 'equality', 'population', "REAL['certified'] == 121", 149),
        ('module-level', 'equality', 'population', "REAL['shells'] == 7", 150),
        ('module-level', 'membership', 'population', "'artichoke' and 'asparagus' in certified_slugs", 151),
    ],
    'test_frost_anchor_reproduction_gate.py': [
        ('test_frost_anchor_reproduction_gate.py::test_scope_is_not_empty', 'floor', 'population', 'n > 1000', 124),
    ],
    'test_gate_all.py': [
        ('module-level', 'floor', 'population', 'len(cert) >= 114 certified', 43),
    ],
    'test_gate_citation_ratchets_a62_a63.py': [
        ('entry point', 'equality', 'population', "'4 known uncited crops' through POT_CEILING (indirect; detector miss)", 73),
    ],
    'test_gate_plant_dimensions_a59.py': [
        ('module-level', 'floor', 'population', 'len(authored) >= 59 crops carrying a height', 119),
    ],
    'test_gate_planting_layout_a44.py': [
        ('module-level (gate_all clean PASS)', 'equality', 'population', "regex 'inspected 121 certified crops, 135 entries; 121 list-shaped, 0 legacy string; null spacing on 8; presence ARMED; rootstock overrides on 1 crop(s), 5 row(s), ARMED'", 117),
        ('module-level (CERT_FLOOR refusal)', 'equality', 'population', "'inspected 121 certified crops, below the declared floor 122'", 125),
        ('module-level (ENTRY_FLOOR refusal)', 'equality', 'population', "'135' in out", 132),
        ('module-level (T2 rootstock)', 'equality', 'population', "'rootstock overrides on 1 crop(s), 5 row(s), ARMED'", 177),
        ('module-level (T2 rootstock)', 'equality', 'content', 'apple rootstock_options spacing_inches == OWED {M9:[48,96], M26:None, MM106:[144,192], MM111:[168,216], seedling:[216,300]}', 142),
        ('module-level', 'equality', 'content', "microgreens spacing_inches None and planting_layout == []; watermelon layout[0].arrangement == 'hill'", 68),
    ],
    'test_gate_plants_per_pot_a60.py': [
        ('module-level', 'equality', 'content', 'basil container_ok True, plants_per_pot None, no plants_per_pot field_additions record', 53),
        ('module-level', 'equality', 'content', 'plum container_ok is not True', 104),
    ],
    'test_herbaceous_perennial_gate.py': [
        ('module-level', 'floor', 'population', '_seen >= 1', 215),
    ],
    'test_ladder_batch.py': [
        ('test_ladder_batch.py::ReadBriefCarriesTheWholeMeaning::test_the_population_this_protects_is_not_empty', 'floor', 'population', 'len(best_use > 104 chars) > 40', 428),
        ('test_ladder_batch.py::BriefCarriesTheWholeMeaning::test_the_population_this_protects_is_not_empty', 'floor', 'population', 'len(best_use > 150 chars) > 20', 518),
        ('test_ladder_batch.py::TheRosterHasRunOutOfTrueTwins::test_the_roster_is_fully_laddered_and_the_floor_agrees', 'equality', 'population', 'unladdered certified slugs == []', 317),
    ],
    'test_perennial_year_gate.py': [
        ('test_perennial_year_gate.py::LiveCanonical::test_the_perennial_roster_is_thirty_eight', 'equality', 'population', 'len(perennials) == 38', 273),
        ('test_perennial_year_gate.py::LiveCanonical::test_pill_caption_is_now_ZERO_and_for_the_RIGHT_REASON', 'equality', 'population', 'len(pills) == 26', 299),
        ('test_perennial_year_gate.py::LiveCanonical::test_the_gate_still_fires_when_the_defect_is_reintroduced', 'equality', 'content', "len(v) == 2 and 'Squeeze the bud.' in v", 313),
    ],
    'test_pla220_borderline_frame.py': [
        ('test_pla220_borderline_frame.py::test_pla202_exclusion_is_real_and_bounded', 'floor', 'population', 'hit_pairs non-empty (>=1)', 185),
        ('test_pla220_borderline_frame.py::test_coverage_is_reported_not_silently_dropped', 'floor', 'population', 'totals.sources_uncovered_total > 0', 199),
    ],
    'test_problem_id_collision_gate.py': [
        ('test_problem_id_collision_gate.py::Preflight::test_canonical_is_the_pinned_sha', 'equality', 'sha', 'shasum(CANON) == PINNED_SHA (b331e5f2..)', 174),
        ('test_problem_id_collision_gate.py::AuditFixture::test_audit_output_is_exactly_pinned', 'equality', 'population', 'findings == 36, actionable == 12, registered == 24 (+12 named registered pairs)', 339),
        ('test_problem_id_collision_gate.py::AuditFixture::test_the_six_merged_decisions_are_resolved_for_the_right_reason / test_the_two_scoped... / test_the_celery_split... / test_the_nine_known_good... / test_batch24_minted_the_ninth_pair', 'equality', 'content', 'named ids absent/present in live; named pairs flagged-then-registered', 248),
    ],
    'test_promote_pla161_hunt28_declaration.py': [
        ('test_promote_pla161_hunt28_declaration.py::test_the_declaration_is_filed', 'equality', 'content', 'P.FINDING id present exactly once on live lemon', 74),
        ('test_promote_pla161_hunt28_declaration.py::test_the_summary_carries_the_document_read_not_a_conclusion', 'equality', 'content', '7 named fragments in the live summary', 90),
        ('test_promote_pla161_hunt28_declaration.py::test_the_citation_is_still_bare', 'equality', 'content', 'node anchoring url == P.BARE_URL and SOURCE_ID in sources', 110),
    ],
    'test_region_prose_gate.py': [
        ('module-level', 'floor', 'population', '_seen >= 2 (detector miss: a floor under 10)', 245),
    ],
    'test_register_completeness_gate.py': [
        ('module-level', 'floor', 'population', '>= 18 certified crops inspected', 51),
    ],
    'test_reporting_contract.py': [
        ('test_reporting_contract.py::test_campaign_C_still_cannot_report_a_clean_completion_today', 'equality', 'population', '(masked_dec, masked_rows) == (39, 195)  [C_MASKED_DECISIONS/C_MASKED_ROWS :40-41]', 156),
        ('test_reporting_contract.py::test_campaign_C_still_cannot_report_a_clean_completion_today', 'floor', 'population', 'masked_dec > 0', 155),
    ],
    'test_soil_temp_floor_scan.py': [
        ('module-level', 'equality', 'population', 'len(ud) == 6 (the ruled utah_dixie cucurbit hits)', 143),
    ],
    'test_sourced_block_ratchet_gate.py': [
        ('test_sourced_block_ratchet_gate.py::LiveCanonical::test_live_uncited_equals_the_waiver_set_exactly', 'equality', 'population', 'set(live uncited) == set(G.KNOWN) (2634)', 245),
        ('test_sourced_block_ratchet_gate.py::LiveCanonical::test_inspected_population_and_verdict', 'floor', 'population', 'inspected >= G.MIN_INSPECTED (6500, pinned :128); stale == []', 239),
        ('test_sourced_block_ratchet_gate.py::PotSizeSubRule::test_live_pot_population_is_the_known_four', 'equality', 'population', "roster(_CANON)[5] == ['dry-bean','grapefruit','green-beans-bush','orange-navel']", 568),
        ('test_sourced_block_ratchet_gate.py::MatureDimensionsSibling::test_armed_the_live_canonical_cites_every_authored_height', 'floor', 'population', 'len(want) >= 59; cited == want', 212),
        ('test_sourced_block_ratchet_gate.py::LiveCanonical::test_the_tickets_98_slot_present_blocks_are_inside_the_population', 'ceiling (red on growth)', 'population', 'len(slots) <= 98', 269),
        ('test_sourced_block_ratchet_gate.py::PinsAreTheMeasurement::test_waiver_file_is_the_measured_population', 'equality', 'sha', "_KNOWN_DOC['measured_on'] == SHA (00dda31c..); count == 2634", 83),
        ('test_sourced_block_ratchet_gate.py::LiveCanonical::test_per_family_counts / test_every_certified_crop_has_at_least_one_waived_block', 'equality', 'population', 'family counts of KNOWN == FAMILY_COUNTS; crops in KNOWN == 121', 251),
        ('test_sourced_block_ratchet_gate.py::MatureDimensionsSibling::setUp', 'equality', 'content', 'carrot mature_height_ft and mature_spread_ft are None', 149),
    ],
}

# file -> why it is not a live pin (REPLAY / DOC_ONLY / SYNTHETIC / HISTORICAL / SCRATCH_DERIVED / CONTENT)
EXEMPT = {
    'test_promote_pla673_d.py': 'REPLAY: its POST_SHA and populations are this promote\'s own output over promote_fixture.pre_state(aaf004a2), never the live canonical; its gates run on that replayed post-state (PLA-673 part D, 2026-10-06)',
    'test_promote_pla673_b2.py': 'REPLAY: its POST_SHA and populations are this promote\'s own output over promote_fixture.pre_state(3ccc25f1), never the live canonical; its gates run on that replayed post-state (PLA-673 part B2, 2026-10-06)',
    'test_era_switch_safety.py': 'SYNTHETIC: hashes the live canonical only to feed its SHA back as a refused era value; it asserts refusals, never a value of the canonical (PLA-673 B2 go-condition 2, 2026-10-06)',
    'test_promote_pla673_glossary.py': 'REPLAY: its POST_SHA and populations are this promote\'s own output over promote_fixture.pre_state(350eda38), never the live canonical; its gate_all runs on that replayed post-state (PLA-673 glossary, 2026-10-05)',
    'test_promote_pla666_row_figures.py': 'REPLAY: its POST_SHA and populations are this promote\'s own output over promote_fixture.pre_state(afbd4113), never the live canonical (PLA-666 row figures, 2026-10-05)',
    'test_promote_housekeeping60_phase_c.py': 'REPLAY: its POST_SHA and populations are this promote\'s own output over promote_fixture.pre_state(b331e5f2), never the live canonical (housekeeping 60 Phase C, 2026-10-04)',
    'test_live_pin_registry.py': 'DOC_ONLY: the registry\'s own test; its SHA prefix and counts are expectations about the detector and this registry, not about the live canonical',
    'test_apply_patch.py': 'HISTORICAL',
    'test_build_berry_pilot_patch.py': 'HISTORICAL',
    'test_build_corn_family_patch.py': 'HISTORICAL',
    'test_build_region_promote.py': 'HISTORICAL',
    'test_build_rgv_promote.py': 'REPLAY (kickoff 60 B5): builds from the pinned pre-RGV canonical 7e29f4f4 and must equal the committed batch; no longer reads the live file',
    'test_critical_warnings_gate.py': 'REPLAY',
    'test_derive_realized_successions.py': "CONTENT: assertions on named live cells' derived values, not a SHA or a population (ruling 3's definition)",
    'test_dezone_lifted_prose.py': 'REPLAY',
    'test_harvest_duration_gate.py': 'HISTORICAL',
    'test_perennial_harvest_gate.py': 'DOC_ONLY',
    'test_promote_artichoke_findings_key.py': 'REPLAY',
    'test_promote_fruit_trees_generic_basis_caveat.py': 'REPLAY',
    'test_promote_mid_atlantic_cherry_sour_marginal.py': 'REPLAY',
    'test_promote_mid_atlantic_handbook_repoint.py': 'REPLAY',
    'test_promote_mid_south_corrected_repoint.py': 'REPLAY',
    'test_promote_mid_south_fruit_corrections.py': 'REPLAY',
    'test_promote_mid_south_fruit_tree_repoint.py': 'REPLAY',
    'test_promote_mid_south_uada_citation_findings.py': 'REPLAY',
    'test_promote_pla10_planting_layout.py': 'REPLAY',
    'test_promote_pla114_credit_line.py': 'REPLAY',
    'test_promote_pla114_lemon_cold.py': 'REPLAY',
    'test_promote_pla114_six.py': 'REPLAY',
    'test_promote_pla155_vce.py': 'REPLAY',
    'test_promote_pla156_corn.py': 'REPLAY',
    'test_promote_pla156_corn_fix.py': 'REPLAY',
    'test_promote_pla157_zinnia_triggers.py': 'REPLAY',
    'test_promote_pla199_titles.py': 'REPLAY',
    'test_promote_pla464_rootstock_array.py': 'REPLAY',
    'test_promote_pla465_null_rulings.py': 'REPLAY',
    'test_promote_pla465_plant_dimensions.py': 'REPLAY',
    'test_promote_pla580_plants_per_pot.py': 'REPLAY',
    'test_promote_pla7_container_path.py': 'REPLAY',
    'test_promote_pla8_ant_exclusion.py': 'REPLAY',
    'test_promote_pla8_batch25.py': 'REPLAY',
    'test_promote_pla8_catalog_r10.py': 'REPLAY',
    'test_release_verify.py': 'SCRATCH_DERIVED',
    'test_rgv_harness.py': 'SCRATCH_DERIVED (kickoff 60 B5): gate verdicts on a scratch copy of live with an injected defect; no population literal',
    'test_source_catalog_title_gate.py': 'REPLAY',
    'test_zone_order_gate.py': 'DOC_ONLY',
}


def reverify_list():
    """The live pins a promote's data commit must record as "re-verified at <sha>", one line per pin."""
    return [f"{f}::{t[len(f) + 2:] if t.startswith(f + '::') else t} ({k}, {c}) -- {a}"
            for f in sorted(LIVE_PINS) for t, k, c, a, _l in LIVE_PINS[f]]


if __name__ == "__main__":
    lines = reverify_list()
    for line in lines:
        print(line)
    print(f"\n{len(lines)} live pins in {len(LIVE_PINS)} files; {len(EXEMPT)} detected files exempt", file=sys.stderr)
