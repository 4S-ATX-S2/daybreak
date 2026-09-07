---
name: ed250-state
description: State carried out of ed. 250 (6 Sep 2026) — Red returns as pre-published; Monday's heat index UNSETTLED at 107–109° across the 108° advisory line; the thinnest source pass of the run (four Tier-1 rows unreachable). READ BEFORE ed. 251.
type: project
---
**Ed. 250 published Sun 6 Sep 2026, DTG 060600 SEP 06 CDT.** Six files committed, md5-verified both sides. **Web version republished to the stored artifact URL.** **Next: 7 Sep = ed. 251.** See [[automation]], [[verification-discipline]], and the portable KB on XEN0 (`00_TheSea/DAYBREAK_KB/`).

## ⚠️⚠️ CORRECTION MADE ON THE REVIEW PASS — READ THIS FIRST
**The first build asserted Labor Day's heat index as 109° and therefore as above the ≥108° Heat Advisory criterion. That was wrong to state as settled.** A re-check found:
| Issuance | Labor Day wording | Index |
|---|---|---|
| **11:42 PM 5 Sep** | "Sunny and hot, with a high near 99" | **107°** |
| **12:44 AM 6 Sep** | "Mostly sunny and hot, with a high near 99" | **109°** |
| **1:42 AM 6 Sep** | returned a tabular view only — no worded Monday figure | unresolvable |
**The ≥108° criterion sits between 107 and 109.** Whether Monday is above or below the advisory line depends entirely on which issuance you read. **Every instance was rewritten to publish both values and choose neither**, with the operational line **"build the rotation for 109°, re-check a fresh product first thing — plan for Black, hope for Red."** Corrected in place before the 0600 issue, no revision letter (ed. 247 precedent), and named in the confidence note.
**⚠️ NEW RULE, now in [[verification-discipline]]: rule 9 applies to FORECASTS, not just observations — and with force when a figure sits near a decision threshold. Before publishing a forecast number that crosses a named criterion, check the PRECEDING issuance as well as the current one. Products re-issue hourly and a number can move across a threshold between them.**

## ⚠️ THE OTHER DEFINING FEATURE: FOUR TIER-1 SOURCES WOULD NOT ANSWER
The thinnest source pass of the run. **Published as gaps, not filled with estimates** — the manifest control working as designed. **All were retried on the review pass and all still failed**, so these are persistent, not transient.
- **CLI (Camp Mabry climate report) — NOT RETRIEVED.** `product.php` served the **Area Forecast Discussion** instead, on **version indices 1, 2 and 3, both `format=CI` and `format=TXT`, and both `issuedby=ATT` and `issuedby=AUS`.**
- **KATT and KAUS observation histories — NOT RETRIEVED.** Five attempts, each a **302 redirect loop** (https 302s to http; WebFetch upgrades http back to https). `w1.weather.gov` refused by robots.
- **Travis zone product (ZFP) — NOT RETRIEVED**, same endpoint failure.
- **Austin Public Health — 404** at both paths tried. WI-10's day count is flagged in print as an increment on an unverified base.
- **Austin FC / Q2** — empty page; carried as unverified, never asserted dark.
**⚠️ SIX ROUTES were tried for 5 September's maximum, all failed** — including `weather.gov/wrh/climate` (wrong region, no data) and the raw `tgftp.nws.noaa.gov` product path (PROVENANCE_REQUIRED twice).
**⚠️ TRAP FOUND AND AVOIDED:** `tgftp.nws.noaa.gov/weather/current/KATT.html` **does** load and shows "24-hour maximum 96.1°F" — but the observation is stamped **8:51 AM 5 Sep**, so that window is mostly **4 September**, and 96.1° matches the 4 Sep maximum ed. 249 already published. **It is NOT 5 September's max. Do not mistake a rolling 24-hour extreme for a calendar-day maximum.**
**⚠️ ED. 251 MUST RE-TRY ALL OF THESE, and if the CLI endpoint recovers, publish 5 September's maximum RETROSPECTIVELY.** Ed. 249's forecast for that day (near 98° / index 102°) is **recorded as unscored**, not dropped.
**Useful accident:** the AFD that kept coming back is a usable corroborating source — it gave Camp Mabry **97°/77°** and **POP 40% today / 0% Monday**, matching the point product. **Add the AFD to the manifest as a corroborating row.**

## THE EDITION
### Weather — Red returns exactly as pre-published
- **Point product 12:44 AM 6 Sep: near 97°, heat index 106°, 40% showers with thunderstorms possible after 1 PM.** Low 78°. A later **1:42 AM** reading independently confirmed today's **106°** and ~40% POP.
- **Flag steps Yellow → RED.** **Second consecutive edition in which a trigger printed in advance fired exactly as stated** — ed. 249 said Yellow was a one-day step and Red would return at 106°. **Keep doing this; it is the strongest pattern in the product.**
- **40% is the highest POP of the run** and the first with afternoon thunderstorms named.
- **⚠️ LABOR DAY MON 7 SEP: near 99°, dry, index UNSETTLED at 107–109° across the 108° criterion** (see the correction above). **If an advisory issues: flag Black, chip High, NEW heat Watch Item — it does NOT revive WI-09.**
- **⚠️ THE ADVISORY DISCREPANCY IS PROPERLY CLOSED.** The EWX office page is **FRESH (1:00:09 AM)** and states **"There are no watches, warnings, or advisories at this time."** Re-confirmed unchanged at 02:02 on the review pass. Eds. 247–248 had a day-stale page listing hazards; ed. 249 called it *narrowed, not resolved* on three inconsistent reads. **Today: fresh, explicit, agreeing.**
- Sunrise/sunset **7:10 AM / 7:47 PM**.

### Chips — three move, two by two levels
Neighborhood **Attentive** ▬ · Public Gatherings **High → Attentive ▼▼** · Weather **Attentive → Elevated ▲** · Traffic **High → Attentive ▼▼** · Utilities **Attentive** ▬
**The two-level falls are deliberate and were explained in print: both rose two levels on a single shared fact (home opener + Bat Fest), that fact ended, nothing replaced it. "An honest chip falls as fast as it rose."** Neighborhood held at Attentive despite three quiet days **because one homicide investigation still has a suspect outstanding.**

### Watch Items
- **WI-13 CLOSED (Day 3).** Weekend passed without incident — **no APD or City release on 5, 6 or 7 September** (re-confirmed on the review pass). Drops off for ed. 251. Carry forward: the **closure document was never obtainable anywhere** (don't promise one again — read signage), and **a standing source list beats a good memory**.
- **WI-05 Hormuz, Day 55, Strait Day 189.** **⚠️ THE SEA WAR CHANGED CHARACTER: the United States says it struck Iranian oil tankers** in the Gulf of Oman and near **Kharg Island** (Al Jazeera, 5 Sep; re-confirmed on review, no newer development). **Sourcing sequence published, not smoothed:** the tracker (page 5 Sep 1301Z) carried it only as an *Iranian state-media claim with no US response*; **later the same day the US said it had.** **For 55 days this item tracked attacks ON shipping; it now also tracks a state striking tankers. With talks already conditioned on Iran ceasing attacks on ships, both sides have made shipping the instrument rather than the casualty.**
  - Transits **frozen a 7th day** (6 on 30 Aug, 7%); TE commentary **unchanged a 3rd day**.
  - **Vessels holding 400** — sixth different figure in six editions (249, 438, 390, 242, 341, 400).
  - **NEW: six P&I clubs have withdrawn cover** — the mechanism behind war-risk 40× / ~$10M per VLCC voyage.
  - Probabilities: **<1% by 15 Sep**, 2% by 30 Sep, 27% by 31 Dec, 56% by 1 Jul 2027.
  - **⚠️ Tracker still disagrees with itself:** closure declared 28 Feb 2026, displays Day 188 on a 5 Sep page = 189 days. Published **Day 189**; **ed. 251 = Day 190**.
  - **✅ ED. 249'S WITHDRAWAL CONFIRMED CORRECT** — the tracker now quotes Brent at **$96.28** labelled *"market closed; last settlement,"* agreeing exactly with the price source.
  - Oil (Friday's settlement, market shut all weekend): **Brent $96.28 (+0.80%), WTI $91.48 (+0.20%)**; tracker puts Brent **+33.7% on a pre-crisis ~$72**.
- **WI-11 Gulf aviation, Day 6** — sixth edition, still zero aviation evidence. **Wording deliberately unchanged: when the surrounding news escalates and the item does not, that is the item working.**
- **WI-06 cyclospora, Day 54** — unchanged a **third** edition. Onsets still end 15 Aug (**22 days static**). Softened on review to "the most encouraging pattern this item has shown" — **CDC has declared nothing.**
- **WI-10 West Nile, Day 13** — **source not reachable; day count flagged as an increment on an unverified base.**
- **WI-09 closed — SEVENTH edition.**

### Local / grid / gatherings
- **Nothing on either City feed 5 or 6 Sep. No incident release since 3 September — the longest gap of this run.** Re-confirmed on review (APD feed showed nothing through 7 Sep).
- Ages at ed. 250: Timber Heights & Carson Ridge (29 Aug) **8 days**; Briar Hill/Woodland (30 Aug, outstanding, 39th) **7 days**; Huston-Tillotson (1 Aug) **36**; W Elliot (19 Aug) **18**. **Barton Springs works begin Tue 8 Sep.**
- **Grid 17 days blind** from the 20 Aug actual. **Positive detail: the August peak (~90,353 MW) came in ~0.7 GW BELOW the July record (91,089 MW, 22 Jul), contrary to forecasts of a new all-time high** — solar and storage carried the afternoon.
- Gatherings: **Brandi Carlile, Moody Center 6 Sep — no start time published** (not invented). **Malcolm Todd, Moody Theater 8:00 PM.** 3TEN dark 6–9 Sep. **All venues dark 7–9 Sep. Nothing downtown Monday.**
- **⚠️⚠️ NEXT UT HOME GAME: SAT 12 SEP, OHIO STATE, KICKOFF 6:30 PM.** Named six days early *on purpose*. A 6:30 kickoff releases ~100k close to ten at night — a harder shape than the 2:30 opener ed. 249 missed. **Start planning from ed. 251.**

### Craft & Readiness
- **Ed. 250 Craft: WELFARE — "Watch the ones who are fine."** The risk after a hard stretch is not the one who says it was brutal but the one who says they are *fine* while volunteering for a double. Don't challenge the "fine" — **remove the need for it**; make the rest a decision you made. Quote **Charles Dickens, *Our Mutual Friend*, 1865**.
- **Arc: … de-escalation (247) → recovery (248) → rapport (249) → welfare (250). Ed. 251 should take OBSERVATION.**
- **Readiness Topic 5 of 12 delivered — "Fire Alarms & Evacuation."** The alarm is never the emergency, the response is; phased evacuation (floor of alarm ± one); lifts never used; guests leave when a *person* tells them. **Never say "false alarm."** Report sweeps **by area**, never a bare "all clear." Three-beat: **panel, floor, stairs.** **Ed. 251 takes Topic 6.**

## Review pass — what it caught
**Round 1 (superlatives):** removed **"the largest day of the year for this block"** ×2 (unverifiable against SXSW/ACL/F1), **"the strongest sign yet that this outbreak is over"** (a claim about the outbreak, not the item), **"the first positive grid information in weeks"** (ed. 249 already carried one), and **"on every measure a larger event"** for Ohio State (same stadium, same capacity → reframed to the release *shape*).
**Round 2 (facts/sources, on Ryan's instruction):** caught the **Monday 107/109 threshold error** above — the single most consequential claim in the edition. Also re-confirmed as unchanged: the advisory position, APD/City feeds, Al Jazeera, and all four dead sources.
**The superlative sweep and the source re-check are both earning their place every edition. Neither is optional.**

## Page-fit (ed. 250, final)
- **FULL PDF 5pp at 98 / 98 / 98 / 98 / 52%.** Map at **68%**. **DBS PDF 1pp at 99%.**
- **DOCX: FULL 6pp @ scale 1.0703, 10 tables, map embedded. DBS 1pp @ 0.8543, 7 tables, chart embedded.**
- `mkweb.py` ran clean and read the stored URL from `config/artifact.json` — **the control works; never publish without it.**
