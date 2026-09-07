# DAYBREAK BRIEF — PORTABLE KNOWLEDGE BASE
### Feed this whole folder to a fresh Claude instance to reproduce the product.

**Product:** a daily security/awareness brief for Four Seasons Hotel Austin, produced by the
ATX Security Office (Ryan Pair, Rowan Risk Solutions).
**Two deliverables, six files, every day:**
- `DaybreakBrief_FULL_YYYYMMDD` — 12 sections, **5–6 pages**
- `DaybreakBrief_DBS_YYYYMMDD` — one-page summary for the DBS & Guest Experience distribution
- each in **HTML + PDF + DOCX**

---

## THE OPENING PROMPT — paste this to a new Claude instance

> You are producing the Daybreak Brief, edition ATX-DB-2026-NNN, for <DATE>.
> Read every file in this folder before you start. In order:
> `01_SOURCE_MANIFEST.md`, `05_VERIFICATION_RULES.md`, `03_HOUSE_STYLE.md`,
> `02_RUNBOOK.md`, `04_PIPELINE.md`, then `state/LATEST_STATE.md`.
> Use `templates/` as the build base — copy the previous edition's HTML and edit it, never
> start from scratch.
> **Fetch every Tier-1 source in the manifest before writing a word.** If a source cannot be
> reached, publish "not verified this pass" and name it in the confidence note.
> Then build, render, LOOK at every page, run the numeric audit, and only then deliver.

**Edition number = day-of-year.** `date -d YYYY-MM-DD +%j` → that's the edition (5 Sep 2026 = 248 → ed. 249).
DTG format: `DDHHMM MON DD CDT`, e.g. `050600 SEP 05 CDT`.

---

## THE FIVE THINGS THAT MOST OFTEN GO WRONG

| # | Failure | Control |
|---|---|---|
| 1 | **A whole event is missed** (UT home game, ed. 249) | `01_SOURCE_MANIFEST.md` — fetch the list, don't judge |
| 2 | **A figure is published that was never retrieved** | numeric audit: every number names the call that produced it |
| 3 | **A superlative with no source** ("the eighth time", "the most ever") | audit covers *first / most / highest / nth time* too |
| 4 | **A "discrepancy" that's just two different hours** | compare source TIMESTAMPS before flagging a conflict |
| 5 | **DOCX ships broken because nobody looked at it** | render every artifact to PNG and *view it* before delivery |

---

## FOLDER MAP

```
DAYBREAK_KB/
├─ 00_START_HERE.md        ← you are here
├─ 01_SOURCE_MANIFEST.md   ← the anti-miss control. READ FIRST.
├─ 02_RUNBOOK.md           ← step-by-step production
├─ 03_HOUSE_STYLE.md       ← voice, sections, chips, flag bands, Craft/Readiness rotation
├─ 04_PIPELINE.md          ← render + page-fit + DOCX technical rules
├─ 05_VERIFICATION_RULES.md← the 11 hard rules, written from real published errors
├─ scripts/                ← render.js, measure.sh, mkdocx.py, mkdocx.js, mkmap.js, autotune.py
├─ templates/              ← latest FULL + DBS HTML (the build base)
├─ state/                  ← LATEST_STATE.md — what the next edition must carry forward
└─ team/                   ← TEAM_GUIDE.md — plain-English guide + FAQ for hotel staff
```

## NON-NEGOTIABLES
1. **Never publish a figure not retrieved this session.**
2. **Never call the Strait of Hormuz "closed" or "shut" in our own voice.** (Retired framing.)
3. **Never assert a distance that wasn't retrieved.**
4. **Publish the local NWS product; name the zone/regional one beside it. Never blend.**
5. **Render and LOOK at every page before delivery.**
