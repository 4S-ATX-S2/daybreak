# LATEST STATE — carried out of ed. 250 (Sun 6 Sep 2026). READ BEFORE ed. 251.

**Next edition: Mon 7 Sep 2026 = ATX-DB-2026-251.** DTG `070600 SEP 07 CDT`. **Monday 7 Sep is Labor Day.**

## ⚠️ READ FIRST — the correction ed. 250 made on its own review pass
The first build asserted **Labor Day's heat index as 109°** and therefore **above the ≥108° Heat
Advisory criterion.** Re-check of consecutive issuances:

| Issuance | Monday wording | Index |
|---|---|---|
| 11:42 PM 5 Sep | "Sunny and hot, with a high near 99" | **107°** |
| 12:44 AM 6 Sep | "Mostly sunny and hot, with a high near 99" | **109°** |
| 1:42 AM 6 Sep | tabular view only, no worded figure | unresolvable |

**The criterion sits between them.** Published as *"unsettled 107–109°, straddling the line; build for
109°, re-check first thing — **plan for Black, hope for Red**."* Corrected in place before the 0600
issue, named in the confidence note (ed. 247 precedent).
**→ ED. 251'S FIRST ACT IS TO RE-READ THE POINT PRODUCT AND SETTLE THIS.** If an advisory has issued:
**flag Black, Weather chip High, open a NEW heat Watch Item — do NOT revive WI-09.**
This is now **rule 12** in `05_VERIFICATION_RULES.md` and **gate G14** in `01_SOURCE_MANIFEST.md`.

## ⚠️ FOUR TIER-1 SOURCES WERE UNREACHABLE ON ED. 250 — RE-TRY ALL OF THEM
Published as explicit gaps, nothing estimated. All were retried on the review pass and all still failed,
so treat them as persistent, not transient.

| Row | Source | Failure mode on ed. 250 |
|---|---|---|
| 4 | CLI Camp Mabry | `product.php` served the **AFD instead**, on versions 1/2/3, `format=CI` and `TXT`, `issuedby=ATT` and `AUS` |
| 5, 6 | KATT / KAUS obs history | **302 redirect loop** (https→http, WebFetch upgrades back). `w1.weather.gov` refused by robots |
| 2 | Travis zone product (ZFP) | same endpoint failure |
| 12 | Austin Public Health | **404** at both paths |

- **⚠️ IF THE CLI RECOVERS, PUBLISH 5 SEPTEMBER'S MAXIMUM RETROSPECTIVELY.** Ed. 249's forecast for
  that day (near 98° / index 102°) is recorded **unscored**, not dropped. Six routes were tried and
  all failed.
- **⚠️ TRAP:** `tgftp.nws.noaa.gov/weather/current/KATT.html` **does** load and shows a "24-hour
  maximum 96.1°F" — but it is stamped **8:51 AM 5 Sep**, so that window is mostly **4 September**, and
  96.1° matches the 4 Sep max ed. 249 already published. **A rolling 24-hour extreme is not a
  calendar-day maximum.**
- **Useful accident:** the AFD that kept appearing is a real corroborator — Camp Mabry **97°/77°**,
  **POP 40% today / 0% Monday**, matching the point product. **It is now manifest row 23.**

## Watch Items — ages step by ONE
| Ref | Item | First noted | Age at ed. 250 | Status |
|---|---|---|---|---|
| WI-05 | Strait of Hormuz | 13 Jul | Day 55 · Strait Day 189 | Open · **character changed — see below** |
| WI-06 | Cyclospora (iceberg) | 15 Jul | Day 54 | Monitoring — unchanged a 3rd edition |
| WI-10 | West Nile — Travis | 25 Aug | Day 13 | Monitoring — FULL only · **day count is an increment on an UNVERIFIED base** |
| WI-11 | Gulf aviation / guest travel | 1 Sep | Day 6 | Monitoring — **6 editions, zero aviation evidence** |
| WI-13 | Bat Fest / Labor Day weekend | 4 Sep | Day 3 | **CLOSED in ed. 250 — drops off** |
| WI-09 | (heat) | — | — | **CLOSED, 7th edition** |

## Forecast handoff
- **Sun 6 Sep published: near 97°, heat index 106°, 40% showers with thunderstorms after 1 PM**, low 78°.
  Confirmed independently at 1:42 AM. **40% is the highest POP of the run**, first with storms named.
- **Flag stepped Yellow → RED, exactly as ed. 249 pre-published.** Second consecutive edition in which
  a trigger printed in advance fired as stated. **Keep doing this — it is the strongest pattern in the product.**
- **Mon 7 Sep: near 99°, DRY, index UNSETTLED 107–109° (see above).**
- **The EWX advisory discrepancy is properly CLOSED.** The office page was **fresh (1:00:09 AM)** and
  said *"There are no watches, warnings, or advisories at this time"*; re-confirmed unchanged at 02:02.
- Sunrise/sunset **7:10 AM / 7:47 PM**.
- Heat run: 100/100/100 (29–31 Aug) · 101 (1 Sep) · 103 (2 Sep) · 102 (3 Sep) · 96 (4 Sep) · **5 Sep unscored**.
- **Overnight minimums have not come down with the days** — 80° on 3–4 and 4–5 Sep.

## Chips at close of ed. 250
Neighborhood **Attentive** ▬ · Public Gatherings **Attentive ▼▼** · Weather **Elevated ▲** ·
Traffic & Arrivals **Attentive ▼▼** · Utilities **Attentive** ▬
*The two-level falls were deliberate and explained in print: both rose two levels on one shared fact
(home opener + Bat Fest), that fact ended, nothing replaced it — **"an honest chip falls as fast as it
rose."** Neighborhood held at Attentive because one homicide investigation still has a suspect outstanding.*

## Events handoff
- **All venues dark 7–9 Sep. Nothing downtown Monday.** 3TEN dark 6–9 Sep.
- **Mon 7 Sep Labor Day** — City offices and municipal facilities closed; personal watercraft ban on
  **Lake Austin** (not Lady Bird Lake).
- **⚠️⚠️ NEXT UT HOME GAME: Sat 12 Sep, OHIO STATE, kickoff 6:30 PM.** Named six days early on purpose.
  **A 6:30 kickoff releases ~100k close to ten at night — a harder shape than the 2:30 opener ed. 249 missed.**
  Do **not** call it "a larger event" (same stadium, same capacity) — the *release shape* is the story.
- **Barton Springs Pool retaining-wall works begin Tue 8 Sep.**
- **Q2 Stadium / Austin FC — page empty, still unverified. Not asserted dark.**

## Rotation
- **The Craft, ed. 251: OBSERVATION.** (250 welfare, 249 rapport, 248 recovery, 247 de-escalation.)
- **Readiness, ed. 251: Topic 6 of 12.** (5 was Fire Alarms & Evacuation; 4 was Crowds/Capacity/Egress.)

## Open threads
- **⚠️ HORMUZ CHANGED CHARACTER:** the **United States says it struck Iranian oil tankers** in the Gulf
  of Oman and near **Kharg Island** (Al Jazeera, 5 Sep; unchanged on review). The tracker carried it only
  as an Iranian state-media claim; the US later said it had. **For 55 days this item tracked attacks ON
  shipping; it now also tracks a state striking tankers.** With talks already conditioned on Iran ceasing
  attacks on ships, **both sides have made shipping the instrument rather than the casualty.**
- Transits **frozen a 7th day** (6 on 30 Aug, 7%); TE commentary unchanged a 3rd day. **Vessels holding 400**
  — sixth different figure in six editions (249, 438, 390, 242, 341, 400). **Six P&I clubs have withdrawn
  cover** — the mechanism behind war-risk 40× / ~$10M per VLCC voyage.
- Oil (Friday settlement, market shut all weekend): **Brent $96.28 (+0.80%), WTI $91.48 (+0.20%)**;
  tracker puts Brent **+33.7%** on a pre-crisis ~$72. **Ed. 249's withdrawal of the "direction conflict"
  was confirmed correct** — the tracker now quotes $96.28 labelled *"market closed; last settlement."*
- **Tracker still disagrees with itself**: closure declared 28 Feb 2026, displays Day 188 on a 5 Sep page
  (= 189). Ed. 250 published **Day 189**; **ed. 251 = Day 190.**
- **CDC unchanged a third edition; onsets still end 15 Aug (22 days static). CDC has declared nothing** —
  do not write that the outbreak is over.
- **Nothing on either City feed 5 or 6 Sep. No incident release since 3 September — the longest gap of
  this run.** Re-confirmed through 7 Sep on review.
- Incident ages at ed. 250 (step by one): Timber Heights & Carson Ridge (29 Aug) **8 days** ·
  Briar Hill/Woodland (30 Aug, **outstanding**, 39th) **7** · Huston-Tillotson (1 Aug) **36** · W Elliot (19 Aug) **18**.
- **Grid blind 17 days** from the 20 Aug actual. Positive detail already published: the August peak
  (~90,353 MW) came in **~0.7 GW BELOW** the July record (91,089 MW, 22 Jul), against forecasts of a new
  all-time high. **Do not re-run it as "the first positive grid news in weeks" — ed. 249 already carried one.**
- **The Bat Fest closure document was never retrievable anywhere.** Don't re-promise it; read signage.

## Corrections not to reintroduce
**From ed. 249:** (1) EWX reads inconsistently — never close a discrepancy on one read. (2) The CLI final
does exist; check both version indices. (3) The tracker's Brent price is a different *hour*, not a
conflict. (4) APD posts non-incident items; "no release" ≠ "no incident."
**From ed. 250:** (5) **Monday's index is 107–109°, unsettled, straddling the ≥108° line — never a bare 109°.**
(6) Superlatives cut: "the largest day of the year for this block" (×2), "the strongest sign yet that this
outbreak is over", "the first positive grid information in weeks", "on every measure a larger event."
