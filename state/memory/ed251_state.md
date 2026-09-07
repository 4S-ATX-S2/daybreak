---
name: ed251-state
description: State carried out of ed. 251 (7 Sep 2026, Labor Day) — the Black-flag tripwire resolved DOWN to 105°; api.weather.gov replaced the product pages and recovered 4 dead sources; Gatherings hit Calm; a superlative-sweep error was caught and published. READ BEFORE ed. 252.
type: project
---
**Ed. 251 published Mon 7 Sep 2026 (Labor Day), DTG 070600 SEP 07 CDT.** Six files built and delivered in-chat. **Web version republished to the stored artifact URL.** **Next: 8 Sep = ed. 252.**
**⚠️ XEN0 WAS UNMOUNTED at commit time — the six ed. 251 files and `cli_bundle.tgz` were NOT written to the drive. They are in the conversation. Re-commit when XEN0 is remounted.**

## ⚠️ THE BIG METHOD CHANGE: api.weather.gov REPLACED THE PRODUCT PAGES
Ed. 250 lost four Tier-1 rows to the rendered NWS pages. **All four answered first try on the service endpoints.** **21/23 sources this morning against 17/23 yesterday.**
| Row | New endpoint |
|---|---|
| 1 | `/gridpoints/EWX/156,91/forecast` |
| 3 | `/alerts/active?point=30.27,-97.74` (replaces the office page that read inconsistently 3× on ed. 249) |
| 2, 4, 23 | `/products/types/{ZFP,CLI,AFD}/locations/{EWX,ATT}` |
| 5, 6 | `/stations/{KATT,KAUS}/observations` (kills the 302 loop) |
**Rule learned: when a source fails repeatedly, question the ROUTE before the source.**

## ⚠️ THE TRIPWIRE RESOLVED DOWNWARD — 105°, NOT 107 OR 109
Ed. 250 published Labor Day as unsettled **107–109°** across the ≥108° criterion and said "plan for Black, hope for Red." **This morning's product, read twice 60s apart, gives near 100° / index 105°** — below the criterion and **below both earlier figures.** **Today was RED, not Black. Zero active alerts.**
**The point to carry: because ed. 250 published a RANGE, ed. 251 published a FACT rather than a correction.** Had it picked 109°, this edition would be retracting. **G14 is now mechanical in the CLI.**

## Observed — BOTH outstanding observations recovered
| Date | Observed | Forecast that called it | Verdict |
|---|---|---|---|
| **5 Sep** | **max 102° at 3:32 PM**, min 77°, 0.00" | ed. 249 said near 98° | **under by 4°** |
| **6 Sep** (prelim) | **max 97° at 2:36 PM**, min 78°, **0.12" rain** | ed. 250 said near 97°, 40% storms | **exact on both** |
- **5 Sep preliminary said 101°, the final said 102° — always pull multiple CLI issuances.**
- **⚠️ 6 Sep figures are the 5:45 PM PRELIMINARY. The final issues ~2 AM. ED. 252 MUST CONFIRM.**
- **⚠️ TRAP: a midnight-issued 6 Sep CLI shows "max 84° at 12:45 AM" — a partial-day product, NOT the daily max.**
- Heat run: 100/100/100 (29–31 Aug) · 101 · 103 · 102 · 96 · **102** · **97**.

## Today's numbers (all double-read, product issued 11:32 PM)
- **Today: near 100°, index 105°, POP 10%, low 79° (index still 103° after dark).** Sunrise/sunset **7:11 / 7:45**.
- **⚠️ TUE 8 SEP: near 101°, INDEX 107° — ONE DEGREE under the criterion. Both reads agree. RE-CHECK ON A FRESH PRODUCT BEFORE 0600.** Wed: near 100°.
- **Hotter air, lower index** than yesterday (100° dry vs 97° humid) — explained in print because it reads as an error.

## Chips
Neighborhood **Attentive** ▬ · Public Gatherings **CALM ▼** · Weather **Elevated** ▬ · Traffic **Attentive** ▬ · Utilities **Attentive** ▬
**⚠️ THE SUPERLATIVE SWEEP CAUGHT A REAL ERROR AND IT WAS PUBLISHED, NOT HIDDEN.** The first build said "**the first Calm chip this brief has carried**" — **FALSE. The 1 September edition carried Calm on this same chip for this same reason (three dark venues).** Found by grepping `chip c-calm` across the edition files on disk. Also cut: "the quietest day this brief has covered", "the first edition in which every venue is dark". **Checking superlatives against the files, not against memory, is what found it.**

## Watch Items — ages step by ONE
| Ref | Age at 251 | Note |
|---|---|---|
| WI-05 Hormuz | Day 56 · Strait Day 190 | **Third character change in three editions** |
| WI-06 cyclospora | Day 55 | **Carried UNREAD** |
| WI-10 West Nile | Day 14 | **APH 404 a 2nd time — REPLACE THE SOURCE** |
| WI-11 Gulf aviation | Day 7 | Unchanged wording, 7th time |
| WI-13 | — | **Closed, dropped off** |
| WI-09 | — | **Closed, 8th edition** |

- **WI-05: from violence toward ADMINISTRATION.** Al Jazeera index, 7 Sep: "**Iran to announce new shipping route in Strait of Hormuz 'in coming days'**", "**Why is Iran planning to enforce a restricted zone near Hormuz?**", Canada "maintain significant pressure", "**Oil prices rise to $97 a barrel**". **⚠️ HEADLINES OFF AN INDEX PAGE — no article was opened; labelled as leads throughout.** Arc: attacks on ships (249) → a state striking tankers (250) → **a state proposing to route and restrict the water (251)**. *An attack is an event; a declared corridor is a claim of authority.*
- **⚠️ THE HORMUZ TRACKER REFUSED US (403, including the browser fallback).** Counts, vessels-holding, war-risk and probabilities are **not verified this pass**. Day 190 is an increment on an unverified base.
- **Oil retrieved fresh, both pages separately: Brent $97.37 (+1.13%), WTI $92.51 (+1.12%)** on a US holiday session — consistent with Friday's $96.28 / $91.48 plus the moves. *Brent's page showed WTI at $92.55 in the same pass, 0.3s apart — a live tick, not a discrepancy.*
- **⚠️ A CDC detail left unreconciled on purpose:** today's landing page says "Updated 27 August" where ed. 250 recorded the investigation page re-dated 3 Sep. **Different pages; not reconciled on a source we did not read.**

## Local / events
- **Nothing on either City feed 5, 6 or 7 Sep. No incident release since 3 September — four days.** City posted 4 Sep: **offices and municipal facilities closed Mon 7 Sep, normal hours Tue 8 Sep**; Lake Austin watercraft ban.
- **All three venues dark 7–9 Sep.** Next: **Tim McGraw, Moody Center, Thu 10 Sep**; Moody Theater same night; 3TEN Fri 11 Sep; J. Cole 14 Sep; Ken Carson 15 Sep.
- **⚠️⚠️ SAT 12 SEP: OHIO STATE AT DKR, 6:30 PM, ON ABC** (confirmed on the athletics schedule; 5 Sep result was **Texas 59–7**). **Kathleen Madigan at the Moody Theater AND Schur at 3TEN the same night — downtown empties twice inside the hour.** **SAT 19 SEP: UTSA at DKR 7:00 PM**, plus the City's **Fiesta de Salud health fair, 11–2, Emma S. Barrientos MACC**.
- Incident ages: Timber Heights & Carson Ridge **9 days** · Briar Hill/Woodland (**suspect outstanding**) **8** · Huston-Tillotson **37** · W Elliot **19**. **Barton Springs works begin Tue 8 Sep.**
- **Grid 18 days blind**; the Texas Power Cost page returned almost no content this pass — **candidate for replacement with a direct ERCOT feed.**

## Craft & Readiness
- **Ed. 251 Craft: OBSERVATION — "On a day when nothing happens, nobody is looking."** No external structure = attention degrades. Observation is a *habit of comparison*, not alertness. Fix the baseline in the first hour; look for what should be there and isn't; say it to one other person. Quote **Arthur Conan Doyle, *A Scandal in Bohemia*, 1891**.
- **Arc: de-escalation (247) → recovery (248) → rapport (249) → welfare (250) → observation (251). Ed. 252 should take HANDOVER or ESCALATION.**
- **Readiness Topic 6 of 12 — "Medical Emergencies & The First Five Minutes"** (AED location, agonal gasping, named person for 911 and for the AED, heat illness as an emergency). **Ed. 252 takes Topic 7.**

## Page-fit
- **FULL PDF 5pp at 99/87/88/97/95%** (pages 2–3 slack from unsplittable table rows — tighten next edition). **DBS PDF 1pp @ 99%.**
- **DOCX: FULL 6pp @ 1.0703 (10 tables, map). DBS 1pp @ 0.8434 (7 tables, chart).**
- Print CSS was tightened slightly on the DBS (`.craft`, `.ready`, `.wi .r`) to hold one page.

## ⚠️ Open items for ed. 252
1. **Confirm 6 Sep's CLI final** against today's preliminary.
2. **Re-check Tuesday's 107°** on a fresh product before 0600.
3. **Replace the Austin Public Health manifest URL** — 404 twice.
4. **Re-try the Hormuz tracker**; if it 403s again, find a second source for transits.
5. **Re-commit the ed. 251 files and `cli_bundle.tgz` to XEN0** once the drive is remounted.
6. **The Duty Manager extension is STILL a placeholder — seventh edition flagged.** One phone call.
