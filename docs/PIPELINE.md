# 04 — PIPELINE (render, page-fit, DOCX)

## Render
`node scripts/render.js FULL DBS` — headless Chromium, `emulateMedia('print')`, Letter, zero margins.
`./scripts/measure.sh <pdf>` prints per-page fill %. Targets: **FULL 5pp** (6pp on heavy editions),
**DBS 1pp at 97–99%**.

## ⚠️ THE PRINT-CSS TRAP (the single biggest page-fit lesson)
**Almost every block hard-codes its `font-size` in the SCREEN css**, so `body{font-size}` inside
`@media print` moves almost nothing. On the DBS a 6.85→6.55px body cut bought only ~0.67in.

**You must add explicit print overrides for each of:**
`.lead` · `.lead .focus` · `.craft .cl` · `.craft .q` · `.wi .r` · `.dv p` · `.out .d p` ·
`.ready p` · `.ready .n` · `.flag .t` · `.cell .lab/.chip/.tr` · `h3.dash` · `.qa .q/.a`

Doing that took the DBS from 2pp to 1pp **and let the type be raised back up** — it ended more
readable than it started. **When a print page overflows: grep the screen CSS for every hard-coded
`font-size` in the overflowing region BEFORE touching `body`.**

## FULL print block (the setting that packs)
`.page` 0.16/0.40/0.03in · body **7.80px**/1.27 · table 7.32px · th 2.2/5 · td 1.9/5 ·
`.lead` 8.20/1.33 · `.conf` 6.20/1.16 · `.src` 6.50px · h2.sec 10.2px · p margin 0 0 3.4px ·
`.callout` 6px 10px · `.craft` 3px/4px 10px · `.contacts .r` 2.1px · **map 58–68%**
Break rules: `.strip,.flag,.map-wrap{page-break-inside:avoid}` and
`.craft p,.craft h4,.ready p,.ready .rgrid>div{page-break-inside:avoid}`.
**`.craft` and `.callout` must NOT be in the avoid list** — that alone cost a whole page once.
**Don't chase body font upward: 7.95 / 8.05 / 8.18px all repack to 6pp even with less ink.**

## DOCX — native builder (`scripts/mkdocx.py`)
LibreOffice and pandoc both produce **ZERO Word tables** from CSS grids. The native builder gives
**7 (DBS) / 10–12 (FULL)** real tables and opens correctly in **Word Online** (the only Word available
on the hotel machines).

**Hard rules:**
1. **A Word paragraph = an HTML *block*.** Every inline descendant (`<b>`, `<em>`, `<span>`, bare text)
   is a **run in the SAME paragraph**. Getting this wrong shatters the lead into one paragraph per bold phrase.
2. **CSS flex/grid rows have no source whitespace** — topbar, classline, strip rows, contact rows need
   separators inserted explicitly or text concatenates.
3. **`mkdocx.js` must run first** — the day-arc chart is drawn in JS and doesn't exist in static HTML.
   **A DBS docx under ~40 KB means the chart was lost.** `mkmap.js` likewise rasterises the FULL's map.
4. **`tblLayout:fixed` is IGNORED unless `w:tblGrid` is rewritten.** `cell.width` + `autofit=False`
   alone does nothing. `fix_widths()` clears and rebuilds gridCols and sets `w:tblW`, and honours the
   `width:NN%` on the source `<th>`s. Fixing this recovered so much dead space the FULL went from
   needing scale 0.86 to fitting at ~1.0.
5. **On tables of ≥6 columns, never shade the status cell** — Word stretches the fill to full row
   height and a tall Watch Item row becomes a black slab. Colour the badge **text** instead.
6. **`autotune.py` binary-searches the type scale** to the page target, range 0.60–1.30.
   **Never hand-pick a scale — it drifts.**

## ⚠️ RENDER AND LOOK
The first native DOCX build shipped broken at 2pp/10pp with a shattered lead. It had been "verified"
by counting tables and characters and **never rendered**. **Structure metrics are not appearance.**
Convert to PDF, rasterise, and view every page before delivery. Every time.

## Other gotchas
- **Sunrise/sunset: use `astral`.** A hand-rolled NOAA formula produced 16:49/4:07 nonsense.
- A **whitespace text node** between `</script>` and `</div>` inside `.page` can generate a line box
  and push a 1-page doc to 2.
- `WebFetch` intermittently returns `PROVENANCE_REQUIRED` — retry once, then move on and say so.

## THE WEB VERSION — `scripts/mkweb.py`
The published team page is the **DBS one-pager**, converted from the print build. The conversion:

1. **Strips the document skeleton.** The Artifact tool supplies its own `<!doctype>/<head>/<body>`;
   leaving ours in produces nested-document behaviour. `mkweb.py` asserts they are gone.
2. **Rewrites the `<title>` to a stable "Daybreak Brief"** — the print file's title carries the
   edition number and date, which must not travel to a page republished daily to one URL.
3. **Adds a screen-only block** — a warm dark ground behind the sheet instead of print-preview grey,
   a drop shadow, and a one-line internal-use header (`.viewnote`, hidden in print).
4. **Adds a scale-to-fit script.** The sheet is a fixed 8.5in with hard-coded px type; on a phone
   that is unreadable. The script scales the whole sheet to the viewport width so it reads like a
   PDF. **Officers will open this on a handset — do not skip it.**
5. **Leaves the entire `@media print` block untouched**, so the same file still prints to exactly 1pp.

**Invariants it enforces (it raises, it does not warn):**
- no `<!DOCTYPE` / `<html` / `<body` / `</html>` survives
- `<div>` open and close counts match

**Publishing:** always pass the `url` from `config/artifact.json`. See `02_RUNBOOK.md` step 14 for
why that is the single most consequential line in the whole distribution path.
