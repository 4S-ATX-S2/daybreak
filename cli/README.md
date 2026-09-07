# `daybreak` — the Daybreak Brief pipeline

Four stages. Each runs on its own, on purpose.

```
  fetch  ──►  facts_<date>.json      walk the manifest, run the gates
              gates_<date>.json      NO MODEL NEEDED
     │
  draft  ──►  prose, chips, Craft    the ONLY stage that needs a model
     │
  build  ──►  6 files (HTML/PDF/DOCX × DBS/FULL)
     │
 publish ──►  web artifact
```

**Most of this brief is not an AI problem.** Fetching 23 sources, checking them
against criteria, and rendering to a page is ordinary code that never forgets.
The model is needed for the writing, and for nothing else. That split is why the
ed. 249 miss cannot happen again: *a loop cannot forget row 20.*

---

## Quick start

```bash
python3 daybreak.py status                     # what has run lately
python3 daybreak.py fetch                      # today; ~60s + the G14 re-read wait
python3 daybreak.py gates                      # re-print the gate report
python3 daybreak.py draft --print-prompt       # the prompt, to paste by hand
python3 daybreak.py build --degraded           # facts-only edition, no model
```

No `pip install`. Standard library only, deliberately: this has to run on a
machine nobody has set up, possibly by someone who is not Ryan.
Node + Playwright are optional — they are used only for the 403 fallback and
for the PDF/DOCX render.

---

## The gates

| Gate | Asks | On failure |
|---|---|---|
| **G13 SOURCE COVERAGE** | Was every Tier-1 row *attempted*? | Row never attempted → `FAIL`, no draft. Row attempted and dead → `DEGRADED`, published as **"not verified this pass"** |
| **G14 THRESHOLD RE-READ** | Is any forecast figure within 3° of a named criterion? | Two reads straddling the criterion → publish **both**, assert neither side |

Neither gate is a judgement. Both are loops.

**G13** exists because ed. 249 shipped without the UT home opener — a ~100k-seat
stadium 1.5 miles away — because "check the venues" was a judgement call rather
than a list. **G14** exists because ed. 250 asserted a 109° heat index, and
therefore "above the 108° advisory criterion", when the issuance an hour earlier
had said 107°.

**A dead source is a published gap. Silence is the only forbidden outcome.**

---

## What `fetch` actually does

Reads `sources.json` — the manifest — and walks it. Nothing is decided at runtime.

| Kind | Rows | Endpoint |
|---|---|---|
| `nws_forecast` | 1 | `api.weather.gov/gridpoints/EWX/156,91/forecast` |
| `nws_alerts` | 3 | `api.weather.gov/alerts/active?point=…` |
| `nws_product` | 2, 4, 23 | `api.weather.gov/products/types/{CLI,ZFP,AFD}/locations/…` |
| `nws_obs` | 5, 6 | `api.weather.gov/stations/{KATT,KAUS}/observations` |
| `http` | 7–22 | plain GET, tags stripped, excerpt + full raw saved |

> **The single biggest reliability win in this whole build.** Four Tier-1 rows were
> unreachable across the whole of ed. 250 — the CLI climate report served the wrong
> product on every version index, and the observation histories 302-looped forever.
> **All of them answer cleanly on `api.weather.gov`.** The HTML product pages are
> not the source; they are a rendering of it. First run of the new fetcher pulled
> 21/23 and recovered 5 September's max — 102° — which ed. 250 had to publish as a gap.

### The 403 fallback
Rows 9 and 20 sit behind bot protection. A row can declare `"fallback": "browser"`,
which gets one Chromium attempt (`browserfetch.js`) before it is called dead. If
*that* fails too the row is marked `needs_manual` and printed in red — because row 20
is the one that must never be silently missing.

---

## Degraded mode — the 4 AM answer

```bash
python3 daybreak.py fetch --date 2026-09-07
python3 daybreak.py build --date 2026-09-07 --degraded
```

Produces `out/brief_<date>.md`: weather table, active alerts, observed maxima,
an explicit **"NOT VERIFIED THIS PASS"** section, and any G14 threshold warning.
No prose, no chips, no watch-item narrative.

It is ugly and it is true and it is on time. **That is a far better failure than
nothing**, and it needs no model, no API key, and no license — a deputy with the
folder and Python can produce it.

---

## Files

```
cli/
  daybreak.py        entrypoint, the four stages, degraded renderer
  collectors.py      one function per source kind; a collector NEVER raises
  gates.py           G13 and G14
  sources.json       THE MANIFEST — 23 Tier-1 rows, Tier-2 triggers, thresholds, calendar
  browserfetch.js    Chromium fallback for the 403 rows
  run_daily.sh       one edition start to finish; exit 3 = degraded edition produced
  deploy/            launchd plist (Mac) · GitHub Actions workflow (cloud)
  out/               facts_*.json, gates_*.json, brief_*.md
  raw/<date>/        exactly what each source returned, for the draft stage to read
  state/             last_forecast.json — the other half of the G14 comparison
```

## Editing the manifest

Adding a source is a one-line edit to `sources.json`. **Do this the moment a miss
is found — that is the whole point of the file.** The `n` is the row number that
appears in the gate report; `rule` is printed back at you when the row dies, so
write it as an instruction to a tired person at 4 AM, not as a description.
