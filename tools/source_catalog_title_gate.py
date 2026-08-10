#!/usr/bin/env python3
"""source_catalog_title_gate -- mint-time title discipline on document-scoped ids (PLA-199, A54).

The defect class (PLA-155's mechanism): source_catalog carried no titles, so a wrong-pub-number
credit was invisible at authoring time and the ornamental-lead scan matched on URL text and
missed its own confirmed case. The fix is structured data (ruling D1: a `title` field, NOT a
name-parenthetical a tool would have to parse -- any title containing parentheses breaks naive
extraction, and "Growing Citrus (Home Garden Series)" is an ordinary extension title).

A54, three checks over data['source_catalog'] (catalog-level; runs identically under every
crop's whole_crop_gate invocation, so a promote minting a titleless id fails the gauntlet):

  1. Every DOCUMENT-SCOPED id (pathed url) carries a non-empty string `title` -- unless it is
     in LEGACY_UNFILLED, the frozen backfill-time exemption list. New ids are never exempt:
     mint-time is when the author has the document open, which is when the title is read OFF
     THE DOCUMENT (never inferred from the id, the URL, or the pub number -- that inference is
     the defect this gate exists to prevent).
  2. An INSTITUTION-ROOT id (bare url, the bare-anchor convention) must NOT carry a title:
     it has no document to state one, so a value there is fabrication (ruling D2, the
     fill-the-shape trap).
  3. LEGACY_UNFILLED must stay honest: an exempt id that is no longer a document-scoped
     catalog id is a stale exemption and flags until the list is pruned. The list may only
     SHRINK (backfilling a member later is fine; it simply stops relying on the exemption).

Wired per the D3 ruling: hard gate AFTER the PLA-199 backfill (101 of 153 document-scoped ids
titled from cached documents), exemptions = exactly the 52 recorded unfilled.
"""
import re

BARE = re.compile(r'https?://[^/]+/?\Z')

# The 52 document-scoped ids recorded UNFILLED by the PLA-199 backfill (2026-08-10), verbatim
# from promote_pla199_titles.UNFILLED: 50 with no cached document, unr_sp2007 (cached body has
# no usable text layer), lsu_agcenter_3363 (cached text layer has body prose but no title line;
# titling it would be URL/pub-number inference). SHRINK-ONLY. Never add a new mint here.
LEGACY_UNFILLED = frozenset({
    'almanac', 'aspca', 'auburn_aces', 'cornell_ext_apple_disease',
    'cornell_ext_apple_fireblight', 'cornell_ext_apple_scab',
    'cornell_ext_strawberry_redstele', 'johnny_seeds', 'lsu_agcenter_3363', 'mo_ext_g6201',
    'mo_ext_g6461', 'msu_bozeman', 'msu_ext', 'msu_radical_roots', 'ncsu_ext_bulb_onions',
    'ncsu_ext_strawberry_anthracnose', 'nws_lzk', 'ohio_state_ext', 'psu_microgreens',
    'purdue_ext_bp132w', 'purdue_ext_foodlink_lavender', 'rutgers_fs044',
    'tamu_agrilife_aggie_spring', 'uada_ext_fsa6001', 'uada_ext_fsa6014', 'uada_ext_fsa6103',
    'uc_anr_8100', 'uc_ipm_citrus_timings', 'uc_mg_marin_citrus', 'uc_mg_sacramento_gn127',
    'ucanr_ext_8256', 'ucanr_ext_woolly_apple_aphid', 'ucanr_slo_mg', 'ucce_kern_kc9382',
    'ucce_placer_nevada_31_018c', 'ucce_riverside_citrus_qa', 'ucd_postharvest',
    'uf_ifas_hs764', 'uf_ifas_leon', 'uf_ifas_nwdistrict', 'uga_b577',
    'uga_c1014_sweet_potato', 'uga_c1232', 'uiuc_ext', 'umaine_ext_2184', 'umass_ext',
    'umn_ext', 'umn_ext_apple_scab', 'umn_ext_edible_flowers', 'unr_sp2007', 'uscrn',
    'weatherkit',
})


def _doc_scoped(entry):
    url = entry.get('url')
    return isinstance(url, str) and not BARE.match(url)


def title_violations(catalog):
    """All A54 violations over a source_catalog dict, as human-readable strings.
    Every message names A54 so an unexpected red is traceable to this gate (PLA-157 rule)."""
    out = []
    for cid in sorted(catalog):
        entry = catalog[cid]
        has_title = 'title' in entry
        if _doc_scoped(entry):
            if has_title:
                t = entry['title']
                if not isinstance(t, str) or not t.strip():
                    out.append(f'A54: {cid}: title is not a non-empty string ({t!r})')
            elif cid not in LEGACY_UNFILLED:
                out.append(
                    f'A54: {cid}: document-scoped id without a title -- read it off the '
                    f'document itself, never from the id/URL/pub number (PLA-199)')
        elif has_title:
            out.append(
                f'A54: {cid}: institution-root id carries a title -- a bare anchor states '
                f'no title; a value here is fabrication (PLA-199 D2)')
    for cid in sorted(LEGACY_UNFILLED):
        if cid not in catalog or not _doc_scoped(catalog[cid]):
            out.append(
                f'A54: {cid}: stale exemption -- LEGACY_UNFILLED names an id that is no '
                f'longer a document-scoped catalog id; prune the list (PLA-199)')
    return out
