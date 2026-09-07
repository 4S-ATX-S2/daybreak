# QUICK CARD — one edition, start to finish
*Print this. Everything else in this folder is explanation; this is the doing.*

---

## The 25-minute path

```bash
cd 1_RUN/cli
python3 daybreak.py fetch          # walks 23 sources, runs both gates    ~2 min
python3 daybreak.py gates          # re-read the gate report              read it
python3 daybreak.py draft          # or --print-prompt to paste by hand
python3 daybreak.py build          # six files
python3 daybreak.py publish        # web version → the STORED url
```

**Before drafting anything, read `3_STATE/LATEST_STATE.md`.** Watch-item ages step by
exactly one. Corrections listed there must not be reintroduced.

---

## Reading the gate report

| Status | Means | Do |
|---|---|---|
| `G13 PASS` | all 23 answered | carry on |
| `G13 DEGRADED` | some tried and dead | **publish each as "not verified this pass"** and name it in the confidence note |
| `G13 PARTIAL` | you ran `--rows` | **not publishable** — re-run without `--rows` |
| `G13 FAIL` | a row was never attempted | **the build is broken.** Do not draft |
| `G14 PASS` | figures near a criterion agree across two reads | safe to assert |
| `G14 STRADDLE` | two reads land either side of a criterion | **publish both, assert neither.** "unsettled X–Y, straddling the line" |

---

## Today's numbers — the standing checks

```
edition no.  = 250 + (today − 2026-09-06)
DTG          = DDHHMM MON DD CDT          e.g. 070600 SEP 07 CDT
heat flag    Green normal · Yellow 91–102 · Red 103–115 · Black advisory or 115+
advisory     ≥108° index or ≥103° air     warning ≥113° index or ≥105° air
```

**A band reading is not an advisory.** Say the flag and the advisory status separately —
staff conflate them, every time.

**If an advisory issues:** flag Black · Weather chip High · open a **NEW** heat Watch Item.
It does **not** revive WI-09.

---

## The five chips

`Calm · Attentive · Elevated · High · Severe`

An honest chip **falls as fast as it rose**. If two chips went up two levels on one shared
fact and that fact ended, they both come back down two — say so in print rather than
letting it look like an overcorrection.

---

## The verification sweep — before you deliver

| ✓ | Check |
|---|---|
| ☐ | Every number traces to a tool call **this session** |
| ☐ | Observed vs forecast is right, **everywhere the number is reused** |
| ☐ | Both City feeds checked **separately** (general ≠ police) |
| ☐ | Publication **year AND day** checked on anything a date search returned |
| ☐ | Local vs zone figures named separately, never blended |
| ☐ | Unreachable sources printed as gaps, not omitted |
| ☐ | **Superlatives**: first / most / highest / strongest / nth time — sourced or cut |
| ☐ | Watch-item ages step by exactly one |
| ☐ | `grep -o 'ATX-DB-2026-[0-9]*'` — consistent everywhere including `<title>` |

**Check superlatives against the files in `5_EDITIONS/`, not against memory.** That is how
ed. 251 caught itself claiming "the first Calm chip this brief has carried" when the
1 September edition had already used it.

---

## Page-fit targets

```
FULL   5 pages, ~98% fill per page      DBS   1 page, ~99%
DOCX   FULL 6pp · DBS 1pp               autotune.py binary-searches the type scale
```

- **Measure before you trim.** `bash 4_BUILD/scripts/measure.sh <file>.pdf`
- **A page showing 1–2% ink is the footer alone spilling.** Shrinking the footer will not
  fix it; body font-size **and** page padding together will.
- **When the edition is genuinely longer, cut type, not reporting.**
- Never hand-pick a DOCX scale — run `autotune.py`.

---

## Delivery

```
SendUserFile each of the six  →  commit to the folder  →  md5 BOTH sides
```

**Do not report delivery until the hashes match.** Use `md5sum` on the device VM — it is
Linux, not macOS, despite the machine being a Mac.

**Web version: republish to the URL stored in `4_BUILD/config/artifact.json`.** Publishing
without it makes a new artifact and the team's bookmark dies.

---

## When it all goes wrong at 4 AM

```bash
python3 daybreak.py fetch
python3 daybreak.py build --degraded
```

Facts-only brief: weather table, alerts, observed maxima, an explicit **NOT VERIFIED THIS
PASS** section, any threshold warning. No prose, no chips, no narrative. **No model, no
API key, no license.**

**It is ugly, it is true, and it is on time — which beats nothing, and beats a polished
brief with one confident wrong number.**
