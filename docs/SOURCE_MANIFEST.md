# 01 — SOURCE MANIFEST (the anti-miss control)

## Why this file exists
On **ed. 249 (5 Sep 2026)** the brief shipped without mentioning that **Texas played its home opener
at DKR that afternoon** — a ~100,000-seat stadium 1.5 miles north, with campus streets closed and
towing enforced. Ryan caught it, not the desk.

**Root cause: "check the venues" was a JUDGEMENT CALL, not a LIST.**
Moody Center, ACL Live, 3TEN, Downtown Austin Alliance and Austin FC were all checked — because
those are the ones that had mattered on previous days. Nothing forced a check of UT football.

**The fix is mechanical: a source is either ON this list and fetched, or the build FAILS.**
Never "check what's on." Always "fetch every row in the manifest."

---

## TIER 1 — MANDATORY EVERY EDITION (build fails if any is missing)

| # | Source | What it gives | Freshness rule |
|---|---|---|---|
| 1 | NWS point forecast, MapClick 30.27/-97.74 | today's high/low/index/POP, hazard headline | **must be issued today**; use a cache-buster, an uncached call returned a 3-day-old product |
| 2 | NWS Travis zone product TXZ192 | zone high/index — **named beside, never blended** | note issuance; day-stale is normal |
| 3 | NWS EWX office page | regional hazard headlines | **day-stale is normal; READ IT 3× — it disagrees with itself** |
| 4 | NWS CLI Camp Mabry (ATT) | yesterday's official max/min/normal/precip | **check `version=1` AND `version=2`** — the final is not always at v1 |
| 5 | KATT observation history | observed hourly heat index (`:51` samples only) | note the last obs time; it freezes for days at a time |
| 6 | KAUS observation history | cross-check only, never substituted | — |
| 7 | Trading Economics — Brent | price, % change, commentary | **re-fetch on the review pass**; header vs commentary often differ, name both |
| 8 | Trading Economics — WTI | price, % change | **fetch separately from Brent, never infer** |
| 9 | Hormuz transit tracker | day count, transits, vessels holding, probabilities, war-risk | sole source for those; flag internal inconsistencies |
| 10 | Al Jazeera news index | Iran / Hormuz / shipping headlines | — |
| 11 | CDC cyclosporiasis investigation | WI-06 figures + page date | note re-dating without data change |
| 12 | Austin Public Health news | WI-10 West Nile | — |
| 13 | **austintexas.gov/news** | City postings | **check separately from APD** |
| 14 | **austintexas.gov/police/news** | APD postings | **check separately — ed. 246 missed 7 items; ed. 249 miscalled a non-incident posting** |
| 15 | ERCOT via Texas Power Cost | grid peak, appeals | count days from the last **actual reading**, not the page edit date |
| 16 | Moody Center calendar | arena events | — |
| 17 | ACL Live — combined listing | Moody Theater | — |
| 18 | ACL Live — **3TEN venue page** | 3TEN | **check separately; the combined listing has omitted 3TEN shows** |
| 19 | Downtown Austin Alliance calendar | downtown events | — |
| 20 | **UT ATHLETICS FOOTBALL SCHEDULE** | **home/away, opponent, kickoff** | **⚠️ THE ED. 249 MISS. MANDATORY.** |
| 21 | **UT Parking & Transportation notices** | lot/garage/street closures, towing | **fetch whenever #20 says HOME** |
| 22 | Austin FC / Q2 Stadium | soccer | if unreachable, publish "unverified", never "dark" |
| 23 | **NWS Area Forecast Discussion (AFD), EWX** | Camp Mabry high/low + POP, reasoning | **corroborating row, added ed. 250** — it is what the CLI endpoint kept serving instead, and it stayed up on the day four Tier-1 rows failed |

## TIER 2 — CONDITIONAL (trigger → fetch)

| Trigger | Fetch |
|---|---|
| Any **Saturday, late Aug → early Dec** | **UT football schedule FIRST, before anything else** |
| UT game is **HOME** | UT parking/closure notice; check kickoff time; stadium ~100k |
| A festival/event is named anywhere | the **City ACE event listing** AND the **organiser's own page** |
| Any event with street closures | the City's closure document + map (link them; if they don't retrieve, SAY SO) |
| Sept–Oct | ACL Fest, F1/COTA (Oct), Trail of Lights (Dec) |
| Legislative session | Capitol events / protests |
| Any tropical system in the Gulf | NHC advisories |

---

## THE SEASONAL CALENDAR — check these BY DATE, not by memory

- **UT football home games**: 5 Sep (Texas State), 12 Sep (Ohio State, 6:30 PM), 19 Sep (UTSA, 7 PM),
  17 Oct (Florida), 24 Oct (Ole Miss), 31 Oct (Mississippi State), 21 Nov (Arkansas). Away/neutral:
  26 Sep Tennessee, 10 Oct Oklahoma (Cotton Bowl), 7 Nov Missouri, 14 Nov LSU, 27 Nov Texas A&M.
  *A home game is the largest predictable crowd event in Austin. It outranks everything else in the brief.*
- **Labor Day** 7 Sep 2026 · **ACL Fest** early Oct · **F1 / COTA** late Oct · **Formula 1 + ACL are
  the two biggest non-football crowd events of the autumn.**

---

## THE FIRST GATE — G13 SOURCE COVERAGE

```
for row in TIER1:
    if row.not_fetched_this_run:  FAIL BUILD
for trigger in TIER2:
    if trigger.fires and not fetched: FAIL BUILD
```
A build that cannot reach a source does **not** silently drop it — it publishes
"not verified this pass" **and says so in the confidence note**. That is always allowed.
**Silence is not.**

---

## THE SECOND GATE — G14 THRESHOLD RE-READ *(added ed. 250)*

```
for figure in DRAFT.forecast_numbers:
    if figure.is_within 3 units of A NAMED CRITERION:
        fetch the PRECEDING issuance of the same product
        if the two issuances straddle the criterion:
            publish BOTH values, assert NEITHER side of the line
```
**Ed. 250's first build asserted Labor Day's heat index at 109° and therefore above the ≥108°
Heat Advisory criterion. The 11:42 PM issuance said 107°. The 12:44 AM issuance said 109°.**
A forecast product re-issues hourly and can move a number across a decision threshold between
reads. **The closer a figure sits to a criterion, the more reads it earns.**
Published form: *"unsettled 107–109°, straddling the line; build for 109°, re-check first thing —
plan for Black, hope for Red."*
