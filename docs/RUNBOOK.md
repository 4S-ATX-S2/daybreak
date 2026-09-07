# 02 — RUNBOOK

## Timing
| Time (CT) | What |
|---|---|
| ~02:20–02:40 | NWS **CLI final** for yesterday issues (check `version=1` AND `version=2`) |
| ~01:20–02:50 | NWS **morning point product** issues |
| **03:15** | **Best build start.** Everything above has landed. |
| 06:00 | DTG / nominal issue time |
| — | One-pager → **Overnight MOD** → internal distribution (the workflow Magee/Storck asked for) |

⚠️ Building before ~02:40 risks the CLI final not existing yet. Ed. 249 built at 01:00–02:05 and
published a "single-issuance" caveat that was wrong — the final had issued at 02:01 at `version=2`.

## Steps
1. **Read** `state/LATEST_STATE.md` — Watch Item ages, carry-forward facts, Craft/Readiness rotation.
2. **Fetch every Tier-1 source** in `01_SOURCE_MANIFEST.md`. Batch calls; the dominant token cost is
   context re-transmission, so 4 fetches in one block beats 4 blocks.
3. **Fire Tier-2 triggers** — especially: *is it a Saturday between late Aug and early Dec? Check UT football.*
4. **Copy the previous edition's HTML** from `templates/` → `DaybreakBrief_FULL_<date>.html` and
   `..._DBS_<date>.html`. Update edition number, DTG, dateline everywhere.
5. **Write the body.** Watch Item ages step by **prior + days elapsed** (not recomputed from scratch).
6. **Render:** `node scripts/render.js FULL DBS`
7. **Page-fit:** `./scripts/measure.sh <pdf>` → FULL 5pp (6pp acceptable on heavy editions), DBS **1pp**.
8. **LOOK at every page.** `pdftoppm -r 88 -png <pdf> p` then view each PNG. Non-negotiable.
9. **Numeric audit** — extract every number and every superlative; each must name its source or be cut.
10. **DOCX:** `node scripts/mkdocx.js` (chart raster) → `node scripts/mkmap.js` (map raster) →
    `python3 scripts/autotune.py` (binary-searches the type scale). **Never hand-pick a scale.**
11. **Verify DOCX:** convert with LibreOffice, check page count, real-table count (7 DBS / 10–12 FULL),
    embedded image count ≥1, and **look at it**.
12. **Deliver** all six files, then **write them to disk** and **md5-verify both sides**.
13. **Update `state/LATEST_STATE.md`** with what the next edition must carry.

## Page-fit levers, in order
1. **The map width %** — the FULL's biggest single lever (68% → 58% recovers ~1 page). Never crop the viewBox.
2. **Hard-coded print font-sizes** — see `04_PIPELINE.md`; `body{font-size}` alone barely moves the DBS.
3. **Structural cuts, in this order:** 4th Watch Item → lowest-value Q&A → 2nd Around-the-Property bullet → condense Craft.
4. **Don't chase body font upward on the FULL** — 7.80px is the setting that packs.

## Delivery
- Six files into the project folder, md5 verified.
- If the machine link is down: deliver in chat, **keep the file_uuids**, commit when it returns.

---

## STEP 14 — THE WEB VERSION (the team's link)
Added 6 Sep 2026, after the claude.ai publish route was chosen over Drive (Drive does not work on
the hotel network).

```
python3 scripts/mkweb.py DaybreakBrief_DBS_<date>.html   # -> brief_web_<date>.html
```
Then publish that file with the Artifact tool, **passing the stored URL** from `config/artifact.json`.

⚠️ **THE FAILURE THAT MATTERS HERE:** the URL belongs to the artifact, not to the file.
**Publishing without the stored `url` creates a BRAND NEW artifact every morning.** The team's
bookmark would keep resolving to whatever day it was created, while fresh links piled up
invisibly behind it. Nobody would notice for days.

- The stored URL lives in `config/artifact.json`. **Read it before every publish.**
- The artifact `<title>` must stay **"Daybreak Brief"** — no date, no edition number. A title that
  changes daily reads as a different page in the gallery and the browser tab.
- The favicon is set **once** and never changed on redeploy — people find the tab by its icon.
- `mkweb.py` asserts the document skeleton was stripped and the divs balance; it raises rather
  than publishing something malformed.

**Order matters:** build → render → verify → **then** mkweb → publish. Never publish a web version
of an edition that has not passed the gates.
