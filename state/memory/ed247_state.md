---
name: ed247-state
description: State carried out of ed. 247 (3 Sep 2026) — heat at the advisory line, the Hormuz throughput corroboration, the missed City postings, Watch Item ages, page-fit numbers, and what ed. 248 must pick up. READ BEFORE ed. 248.
type: project
---
**Ed. 247 published Thu 3 Sep 2026, DTG 030600 SEP 03 CDT.** Six files committed and md5-verified: `DaybreakBrief_FULL_20260903` and `DaybreakBrief_DBS_20260903`, each in **HTML + PDF + DOCX**. **Next: 4 Sep = ed. 248.** Production is being automated — see [[automation]] first.

## ⚠️ STANDING FROM RYAN (3 Sep) — THE NEW DAILY SHAPE
**Every day from now on = the DBS 1PG *and* the FULL multi-page, each in PDF + DOCX + HTML.** Six files per edition. The DBS template is no longer provisional. Keep the pipeline deterministic.

## ⚠️⚠️ DOCX — THE FIRST BUILD SHIPPED BROKEN AND RYAN CAUGHT IT
**Superseding the earlier note in this file:** the LibreOffice HTML-import recipe is **NOT** the one to use, and neither was the first native build. Full detail in [[automation]]; the short version:
- LibreOffice and pandoc both produce **ZERO Word tables** — every CSS grid collapses to stacked paragraphs.
- The first `mkdocx.py` was "verified" by **counting tables and characters and never rendering it**. It shipped at **2pp (DBS) / 10pp (FULL)** with the lead **shattered into one paragraph per bold phrase**, because the walker made a new Word paragraph for every `<b>`.
- **The rule: a Word paragraph = an HTML *block*; every inline descendant belongs in the SAME paragraph as runs.** CSS flex rows (topbar, classline, strip rows, contacts) have no source whitespace and need separators inserted explicitly.
- **`scripts/mkdocx.js` must run first** to rasterise the JS-drawn day-arc chart; a DBS docx under ~40 KB means it was lost.
- Fixed build: **7 (DBS) / 12 (FULL) real Word tables**, **DOCX 1pp / 6pp** against **PDF 1pp / 5pp** — they differ by design, and `build.sh` **auto-tunes the scale** to the target rather than using a hand-picked constant.
- **LESSON: structure metrics are not appearance. Render every artifact and look at it before delivery.** Gate **G12** now enforces DOCX page count, table floor and embedded image.

## ⚠️⚠️ PAGE-FIT — THE BIG LESSON OF ED. 247
**The FULL is PACKING-limited, not volume-limited.** It came in at 6pp with **3.1 in** of overflow while pages 2 and 4 were only 79–81% full — the dead space came from `page-break-inside:avoid` on big blocks, not from too much content.
- **The decisive fix was `.craft`** — remove it from the avoid list and make only its children unbreakable:
  `.strip,.flag,.map-wrap{page-break-inside:avoid;} .craft p,.craft h4,.ready p,.ready .rgrid>div{page-break-inside:avoid;}`
  That alone took 6pp → 5pp, and The Craft still landed whole.
- **Shrinking the FULL's map is the other packing lever** (never crop the viewBox). It went 86% → 72%, then **→ 68%** when late copy was added. The map-wrap is ~2.2 in and unbreakable — it is what pushes the break.
- **⚠️ Do not chase body font upward.** 7.95, 8.05 and 8.18px all repacked to 6pp even with *less* total ink. **7.80px is the setting that packs.**
- **FULL print block (final, 5pp at 99/100/98/99/75%):** `.page` **0.16/0.40/0.03in** · body **7.80px/1.27** · table **7.32px** · th 2.2/5 · td 1.9/5 · `.lead` **8.20/1.33** · `.conf` **6.20/1.16** · `.src` **6.50px** · h2.sec 10.2px · p margin 0 0 3.4px · `.callout` 6px 10px · `.craft` 3px/4px 10px · `.contacts .r` 2.1px · **map 68%**.

## ⚠️ DBS PAGE-FIT — THE `.qa` TRAP
The DBS came in at 2pp with **1.95 in** over, and type cuts did almost nothing — **because `.qa .q` and `.qa .a` are hard-coded at 7.9px in the SCREEN css with no print override**, so shrinking `body` never touched the "If a Guest Asks" column. It also looked wrong: left column 6.08px beside right column 7.9px.
**The fix, and the pattern to reuse:** add `.qa .q{font-size:6.6px;} .qa .a{font-size:6.6px;line-height:1.26;margin:0 0 2.6px;}` in print — that freed enough to raise `body` from 6.08 back to **6.85px**, ending *more* readable than it started and still 1pp at 97%.
- **Structural cuts** (documented order held): dropped the **4th watch item (WI-10)** to the FULL — its action already lived in the Engineering and Security division cells; dropped the **lowest-value Q&A** (the storm one, once Edouard closed) rather than mechanically the 4th; condensed the Craft, flag box, lead and grid bullet.
- **DBS print block (1pp at 97%):** body **6.85px/1.15** · `.page` 0.05/0.26/0.01in · `.masthead{padding:0}` h1 **18.5px** · `.band{margin:0.5px 0}` · `.topbar` 1.4px · `.classline` 1.5px/2px · `.cell` 2/3/1.5px · `.lead` 3px 7px 1.5px · `.wi .r` 1.05px 5.5px · `.dv` 1.2px 4px 1.5px · `.out .d` 1.2px 5px · `.qa` **6.6px** · `.foot` 5.8px/1.18. **Map stays cut** (second edition running).

## The edition's substance — carry forward
- **HEAT IS THE STORY AND IT IS STILL CLIMBING.** **CLI: Camp Mabry 103° on 2 Sep** (max **3:20 PM**, min 76° at 6:05 AM, normal 95°, precip **0.00**) — **corroborated across two issuances agreeing on BOTH value and time** (2:35 AM final, 5:46 PM preliminary). **Fifth consecutive day at or above 100°** (29/30/31 Aug 100°, 1 Sep 101°, 2 Sep 103°); **each of the last three set a new high**. Ed. 246's "near 100°" ran **3° cold**.
- **⚠️ ED. 246's "A PLATEAU, NOT A PEAK" WAS PUBLISHED AS AN EDITORIAL ERROR AND WITHDRAWN.** The 3° miss is the forecast's; the *word* was ours. **The cleanest example yet of correction-vs-revision discipline — keep doing it.**
- **3 Sep: near 102° / index 108°, 20% storms after 4 PM.** **108° IS THE ≥108 ADVISORY CRITERION EXACTLY.** Flag held **Red**, chip **Elevated**, **WI-09 closed for a fourth edition** — with the Black/High/new-item trigger named in print. **Closest the brief has come to Black without crossing.**
- **⚠️ THE ADVISORY DISCREPANCY — reuse this handling.** `weather.gov/ewx` (**day-stale, 10:00 AM 2 Sep**) listed a **Heat Advisory**, and on a 04:07 re-check also a **Flood Watch** — which confirms it was showing yesterday's regional picture. Against that: the **2:42 AM point product** and **1:33 AM Travis zone product** both carried **no hazard headline**, and the City's advisory page **404s**. Published position: *a day-old regional page is not evidence of an advisory for Travis County today* — publish the fresh products' silence and **name the discrepancy rather than resolve it**.
- **Fri 4 Sep: near 98° / index 104° / 30% storms** — first sub-100° day; zone puts Fri and Sat in the **mid 90s**. **Sat 5 Sep near 99°.** ⚠️ Ed. 246's day-old **110° weekend index is WITHDRAWN**. ⚠️ **An index of 104° is still RED (103–115)** — ed. 247 caught a drafted "Red → Yellow" line; **Red holds unless the index verifies at 102° or below.** Gate G3 now enforces this.
- **⚠️ COORDINATE FRESHNESS DID NOT REVERSE** — the four-edition run ended; the **LONG** string was fresh (2:42 AM). **Still fetch both every time.**
- **KATT obhistory FROZE A SECOND TIME** — still ending **02:51 on 2 Sep** after 24 hours. **No city-station index for 2 Sep; recorded as "unavailable at this reading," not unresolved.** **KAUS fresh** (to 01:53): 2 Sep peak air 100°, **index 104°** — **named as the airport's figure, not adopted**; Camp Mabry ran 3° hotter on air the same day.
- Sunrise/sunset 3 Sep **7:09 AM / 7:50 PM**.

## Hormuz — WI-05 Open, Day 52
- **THE INDEPENDENT TRANSIT FIGURE ED. 246 ASKED FOR HAS ARRIVED.** Crude crossing at an estimated **8 million barrels a day** (pre-war ~**20 million**); **Kpler: four tanker crossings on Tuesday, against ten on Monday**. **Ed. 246's retirement of "closed" is vindicated.**
- **⚠️ ATTRIBUTION CORRECTION PUBLISHED:** the 17-million-barrel figure, which ed. 246 gave to **Treasury Secretary Scott Bessent**, is attributed by the same source to **Energy Secretary Chris Wright** — **highest since the war began in late February**. Figure stands; name was wrong.
- **The tracker's transit count FINALLY MOVED**: **6 transits on 30 Aug** vs a stated typical **85/day** = **7%** (the page's own arithmetic), after ten days frozen at 3 on 23 Aug. Page **2 Sep 1305Z**, a day stale. **The day count stays retired — never reintroduce it or the word "shut."**
- **⚠️ ED. 247 DECLINED TO RECONCILE the 8 m bbl/day, the 4 Kpler crossings and the tracker's 6 transits** — three measurements, three methods, three days. **Published all three, converted none. Reuse this; converting between them manufactures a number nobody published.**
- **THE EDITORIAL SPINE:** *"the strait is moving more oil than at any point since February, and this week it killed two seafarers — throughput and safety are not the same measurement."* **Al Jazeera (2 Sep): Saudi Arabia condemns a deadly Iranian attack on a tanker in the strait, two Filipino crew killed.** (3 Sep): **death toll inside Iran 18**; Trump "ready to strike at any time."
- ⚠️ **The source changed its own copy during the morning** on the countries struck: an early reading gave Jordan, Kuwait, Bahrain, Iraq **and the UAE**; the 04:07 reading gave **Bahrain, Jordan, Kuwait and Iraq**. **Published the current reading and said so in print** — rule 10 in practice.
- **Metrics NOT read as signal:** vessels holding **390** (third figure in three editions: 249 → 438 → 390) inside the tracker's own **7-day range 249–997**. Year-end like-for-like **30% → 28% → 27%**. Also shown: 1% by 15 Sep, 3% by 30 Sep; 7-day-avg-transits-over-60 at 3% by 1 Oct, 24% by 1 Jan 2027, 54% by 1 Jul 2027. **The "$4.78/gal" pump price is CONDITIONAL on full closure — always label it.**
- **OIL as finally published (re-verified 04:07, updated in place before the 06:00 issue — no Rev letter): Brent $95.87 (+$0.21, +0.22%); WTI $90.555 (−$0.45, −0.50%). The two grades SPLIT on the session.** Both above $90 a third day; **Brent above $95 for the first time in this brief**. Also: **US crude inventories fell 4.5 million barrels last week, first drop since late July.**
  ⚠️ **Oil moves intraday — always re-fetch both TE pages on the review pass.** The first build published Brent at $95.10 (−0.59%) and the direction had flipped by 04:07.

## Watch Items at close of ed. 247
- **WI-12 CLOSED** — NHC **final advisory** on Edouard (07:00 UTC 3 Sep): inland depression near **32.2°N 95.7°W**, 25 mph, WPC takes over; heavy rain over flooded East Texas **through midday Thursday**; no active Atlantic system threatens the US. Ran one "Closing" entry (badge `b-closed`) and **drops off the register for ed. 248**. Opened and closed inside two editions — a good narrow item.
- **WI-05 Open, Day 52.** *Next:* whether independent counts continue; further attacks on shipping or a Gulf energy/port facility; whether the tracker keeps moving.
- **WI-11 Monitoring, Day 3** — Gulf aviation. **Still zero aviation evidence**; a direct search surfaced only Feb–Jul 2026 closures, all lifted. **Published as: the exposure widened while the aviation evidence stayed at zero.**
- **WI-06 Monitoring, Day 51** — cyclospora, CDC unchanged at 27 Aug (11,458 / 20 states / ≥495 hosp / 2 deaths Michigan; Texas a case state; onsets 14 Jun–15 Aug).
- **WI-10 Monitoring, Day 10** — West Nile; APH still 20 Aug, **fourteen days**. **FULL only — cut from the DBS at trim time.**
- **WI-09 stays closed** — fourth consecutive edition.

## Chips (ed. 247)
Neighborhood **Attentive** ▬ · **Public Gatherings stepped Calm → Attentive ▲** (three dark nights end) · Weather **Elevated** ▬ · Traffic & Arrivals **Attentive** ▬ (**the reason changed, not the level** — Edouard expired, Labor Day getaway + 10 PM release replaced it; reuse this move) · Utilities **Attentive** ▬.

## Local — ⚠️ ED. 246 MISSED SEVEN CITY POSTINGS
**Ed. 246 stated "the City of Austin has posted nothing new since 31 August." Seven items were posted on 1 September.** Withdrawn in print as our own error. **Lesson: check `austintexas.gov/news` AND `austintexas.gov/police/news/` separately every edition.**
The 1 Sep releases, all about **older** incidents:
- **Homicide, 11700 block of Timber Heights Drive** — **Sat 29 Aug 5:34 PM**, case **26-2411173**, **suspect arrested at the scene and charged**, **Austin's 38th homicide of 2026**. ⚠️ **Numbered out of date order** — the 38th (29 Aug) was released two days after the 39th (30 Aug). Flagged in the confidence note.
- **Aggravated assault, 900 Chicon Street (Huston-Tillotson)** — **Sat 1 Aug 12:30 AM**, case **26-2130045**, **a security officer assaulted while removing a trespasser**, minor injuries, suspect at large. **This became The Craft.**
- **Robbery, 200 block of West Elliot Street** — **Wed 19 Aug ~5 AM**, case **26-2310239**, knife displayed, bicycle taken, suspect unidentified, **stated to frequent North Lamar and Georgian Drive**.
- Arrest in a large mail-/bank-card-theft investigation. Plus **Austin Emergency Management's National Preparedness Month kickoff** (used in Readiness), Commons Ford Labor Day parking changes, a community-grants item. **2 Sep: a cold-case DNA release — deliberately not carried.** Nothing new on a 04:07 re-check.
- **Editorial line to reuse: "a burst of postings is not a burst of crime."** Chip held. ⚠️ **Numeric audit caught "four and thirty-three days old" — correct is FIVE to thirty-three** (29 Aug → 3 Sep = 5 days). Also softened "three of the four resolved or historic" to the unarguable **"two of the four already resolved by arrest."** Gate G10 now checks day-counts against dated anchors.
- Standing: Briar Hill/Woodland homicide (30 Aug, case 26-2420956, outstanding, **39th of 2026**) **four days old, nothing added**; **"northeast Austin" is a syndicated characterisation — assert no distance**. Fatal collisions 25/26/27 Aug now **seven to nine days**. Barton Springs works from **8 Sept**.
- ⚠️ **GRID DAY-COUNT BASIS RESOLVED.** The count runs **from the last actual peak reading (20 August)**, not the page's edit date (22 August) — hence 1 Sep = 12, 2 Sep = 13, **3 Sep = 14**. Ed. 247 made the basis explicit in print. Page **retrieved successfully** (refused on ed. 246): *"a page we can read that has nothing new to say is a different failure from a page that refuses us."* 20 Aug peak ~90,353 MW vs record 91,089 MW (22 Jul 2026), no appeal.

## Gatherings — the city restarted
All three venue pages **retrieved successfully** (both ACL Live pages were refused on ed. 246): **Koe Wetzel, Moody Center, 3 Sep 7:00 PM** (do512); **Fragile Rock w/ Flyer Club, 3TEN, 8:00 PM**; **Moody Theater dark 3 and 4 Sep**; **Malcolm Todd, Moody Theater, 5–6 Sep 8:00 PM** — **0.5 mi W and ON the map**, a closer event than the arena. 4 Sep: Johnny Blue Skies (Moody Center 7:00 PM) + Alex Lambert (3TEN 8:00 PM). DAA: nothing downtown tonight. **Q2 not checked — published as "not verified," never asserted dark.**
**Map:** pin 1 gold/live labelled "3TEN live 8 PM · Theater dark"; **off-map north arrow used** (the arena was the night's main variable) at x=205 y=34→8 with a gold triangle head. **Labor Day is Monday 7 September**; the weekend runs 4–7 Sep.

## The Craft — ed. 247
Topic **DE-ESCALATION** — *"The last ten feet"*, anchored (de-identified) in the Huston-Tillotson release: **asking someone to leave is the most dangerous routine task in this work**; give them a way out that doesn't cost their face; name the destination not the judgement; never stand between a person and the exit you're asking them to use; the risk sits in the last ten feet, not the opening line; **"two people and a radio, not a better sentence."** Quote: **Abraham Lincoln, Address to the Washingtonian Temperance Society, Springfield, Illinois, 22 February 1842**.
**Arc: observation → rapport → recovery → de-escalation → welfare → observation → de-escalation. Ed. 248 should take RAPPORT or RECOVERY.** Used quotes now include **Lincoln**.
**Pattern worth reusing: anchor The Craft in a real, local, de-identified incident from that morning's own police releases.**

## Readiness — Topic 2 of 12 delivered
**Medical Response & AED Locations** — *"What we actually have to offer is minutes."* Survival falls ~10%/minute before defibrillation; the clock runs through lobby, lift and corridor. Do This Today: walk to the AED nearest your station and the one nearest the function space, check you can reach it **without a key**, **say its location out loud**. If It Happens: **do not send "someone" — point and name**; 911 then Security Duty Ext 8240; don't move the person; compressions if unresponsive and not breathing normally; **"call, AED, door."** Tied to the City's **National Preparedness Month** kickoff.
**Ed. 248 takes Topic 3 — Severe weather & shelter points.**
