#!/usr/bin/env python3
"""Tests for the shared spelled-temperature scanner + fixer (post-114 §C). Run:
    python3 tools/test_temp_scan.py

WHY: the old per-gate regex (\bdegrees?\s*F\b) missed '90 degrees', bare '50 F', and
'degrees Fahrenheit' -- all shipped. This module widens detection AND provides the fixer, with a
latitude/angle exclusion so onion's '38 to 39 degrees' (latitude) is never touched.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from temp_scan import spelled_temp_hits, convert_temps

# --- spelled_temp_hits: FLAG the shipped forms ---
assert spelled_temp_hits("extreme heat above 90 degrees does the same")      # '90 degrees'
assert spelled_temp_hits("a week of nights below 50 F bolts")                # bare '50 F'
assert spelled_temp_hits("hardy to about 17 degrees Fahrenheit, but")        # 'degrees Fahrenheit'
assert spelled_temp_hits("put them somewhere warm (70 to 80 degrees is ideal)")
assert spelled_temp_hits("countertop at around 60-65 degrees. Don't")
assert spelled_temp_hits("keep near 30 to 35 F at high humidity")            # 'F' after a range

# --- spelled_temp_hits: do NOT flag the correct or the EXPLICIT-latitude forms ---
assert spelled_temp_hits("the ideal 70 to 80°F range") == []                 # already °F
assert spelled_temp_hits("cold below 50°F damages the tomato") == []
assert spelled_temp_hits("grows above about 38 to 39°N") == []               # clarified latitude °N
assert spelled_temp_hits("about 45 degrees north latitude") == []            # explicit "degrees north"
assert spelled_temp_hits("") == [] and spelled_temp_hits(None) == []
# a BARE "38 to 39 degrees" with no N/S marker IS flagged -- it is ambiguous and must be clarified to °N
assert spelled_temp_hits("at latitudes roughly above 38 to 39 degrees")      # onion's unclarified form

# --- convert_temps: rewrite to °F ---
assert convert_temps("above 90 degrees does") == "above 90°F does"
assert convert_temps("nights below 50 F bolts") == "nights below 50°F bolts"
assert convert_temps("hardy to about 17 degrees Fahrenheit, but") == "hardy to about 17°F, but"
assert convert_temps("warm (70 to 80 degrees is ideal)") == "warm (70 to 80°F is ideal)"
assert convert_temps("around 60-65 degrees. Don't") == "around 60-65°F. Don't"
assert convert_temps("near 30 to 35 F at") == "near 30 to 35°F at"
# idempotent + latitude untouched
assert convert_temps("the ideal 70 to 80°F range") == "the ideal 70 to 80°F range"
assert convert_temps("above 38 to 39 degrees north latitude") == "above 38 to 39 degrees north latitude"

print("temp_scan tests: OK")
